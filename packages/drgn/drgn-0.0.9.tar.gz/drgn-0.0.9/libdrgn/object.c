// Copyright (c) Facebook, Inc. and its affiliates.
// SPDX-License-Identifier: GPL-3.0+

#include <assert.h>
#include <inttypes.h>
#include <stdlib.h>
#include <string.h>

#include "drgn.h"
#include "error.h"
#include "language.h"
#include "memory_reader.h"
#include "minmax.h"
#include "object.h"
#include "program.h"
#include "serialize.h"
#include "type.h"
#include "util.h"

LIBDRGN_PUBLIC void drgn_object_init(struct drgn_object *obj,
				     struct drgn_program *prog)
{
	obj->type = drgn_void_type(prog, NULL);
	obj->bit_size = 0;
	obj->qualifiers = 0;
	obj->encoding = DRGN_OBJECT_ENCODING_NONE;
	obj->kind = DRGN_OBJECT_ABSENT;
	obj->is_bit_field = false;
}

static void drgn_value_deinit(const struct drgn_object *obj,
			      const union drgn_value *value)
{
	if (obj->encoding == DRGN_OBJECT_ENCODING_BUFFER &&
	    !drgn_object_is_inline(obj))
		free(value->bufp);
}

LIBDRGN_PUBLIC void drgn_object_deinit_value(const struct drgn_object *obj,
					     const union drgn_value *value)
{
	if (value != &obj->value)
		drgn_value_deinit(obj, value);
}

LIBDRGN_PUBLIC void drgn_object_deinit(struct drgn_object *obj)
{
	if (obj->kind == DRGN_OBJECT_VALUE)
		drgn_value_deinit(obj, &obj->value);
}

/* Copy everything from src to dst but the program, kind, and value. */
static inline void drgn_object_reinit_copy(struct drgn_object *dst,
					   const struct drgn_object *src)
{
	drgn_object_deinit(dst);
	dst->type = src->type;
	dst->qualifiers = src->qualifiers;
	dst->encoding = src->encoding;
	dst->bit_size = src->bit_size;
	dst->is_bit_field = src->is_bit_field;
}

struct drgn_error *
drgn_object_type_encoding_and_size(const struct drgn_object_type *type,
				   enum drgn_object_encoding *encoding_ret,
				   uint64_t *bit_size_ret)
{
	struct drgn_error *err;
	bool is_complete;

	*encoding_ret = drgn_type_object_encoding(type->underlying_type);
	is_complete = drgn_object_encoding_is_complete(*encoding_ret);
	if (is_complete) {
		err = drgn_type_bit_size(type->underlying_type, bit_size_ret);
		if (err)
			return err;
	} else {
		*bit_size_ret = 0;
	}
	if (type->bit_field_size) {
		if (is_complete && type->bit_field_size > *bit_size_ret) {
			return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
						 "bit field size is larger than type size");
		}
		*bit_size_ret = type->bit_field_size;
	}
	return NULL;
}

struct drgn_error *
drgn_object_set_common(struct drgn_qualified_type qualified_type,
		       uint64_t bit_field_size,
		       struct drgn_object_type *type_ret,
		       enum drgn_object_encoding *encoding_ret,
		       uint64_t *bit_size_ret)
{
	type_ret->type = qualified_type.type;
	type_ret->qualifiers = qualified_type.qualifiers;
	type_ret->underlying_type = drgn_underlying_type(qualified_type.type);
	type_ret->bit_field_size = bit_field_size;
	return drgn_object_type_encoding_and_size(type_ret, encoding_ret,
						  bit_size_ret);
}

struct drgn_error *
drgn_object_set_signed_internal(struct drgn_object *res,
				const struct drgn_object_type *type,
				uint64_t bit_size, int64_t svalue)
{
	if (bit_size == 0 || bit_size > 64) {
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
					 "unsupported integer bit size (%" PRIu64 ")",
					 bit_size);
	}
	drgn_object_reinit(res, type, DRGN_OBJECT_ENCODING_SIGNED, bit_size,
			   DRGN_OBJECT_VALUE);
	res->value.svalue = truncate_signed(svalue, bit_size);
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_signed(struct drgn_object *res,
		       struct drgn_qualified_type qualified_type,
		       int64_t svalue, uint64_t bit_field_size)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;
	if (encoding != DRGN_OBJECT_ENCODING_SIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not a signed integer type");
	}
	return drgn_object_set_signed_internal(res, &type, bit_size, svalue);
}

struct drgn_error *
drgn_object_set_unsigned_internal(struct drgn_object *res,
				  const struct drgn_object_type *type,
				  uint64_t bit_size, uint64_t uvalue)
{
	if (bit_size == 0 || bit_size > 64) {
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
					 "unsupported integer bit size (%" PRIu64 ")",
					 bit_size);
	}
	drgn_object_reinit(res, type, DRGN_OBJECT_ENCODING_UNSIGNED, bit_size,
			   DRGN_OBJECT_VALUE);
	res->value.uvalue = truncate_unsigned(uvalue, bit_size);
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_unsigned(struct drgn_object *res,
			 struct drgn_qualified_type qualified_type,
			 uint64_t uvalue, uint64_t bit_field_size)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;
	if (encoding != DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not an unsigned integer type");
	}
	return drgn_object_set_unsigned_internal(res, &type, bit_size, uvalue);
}

static struct drgn_error *
drgn_object_set_float_internal(struct drgn_object *res,
			       const struct drgn_object_type *type,
			       uint64_t bit_size, double fvalue)
{
	if (bit_size != 32 && bit_size != 64) {
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
					 "unsupported floating-point bit size (%" PRIu64 ")",
					 bit_size);
	}
	drgn_object_reinit(res, type, DRGN_OBJECT_ENCODING_FLOAT, bit_size,
			   DRGN_OBJECT_VALUE);
	if (bit_size == 32)
		res->value.fvalue = (float)fvalue;
	else
		res->value.fvalue = fvalue;
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_float(struct drgn_object *res,
		      struct drgn_qualified_type qualified_type, double fvalue)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_set_common(qualified_type, 0, &type, &encoding,
				     &bit_size);
	if (err)
		return err;
	if (encoding != DRGN_OBJECT_ENCODING_FLOAT) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not a floating-point type");
	}
	return drgn_object_set_float_internal(res, &type, bit_size, fvalue);
}

struct drgn_error *sanity_check_object(enum drgn_object_encoding encoding,
				       uint64_t bit_field_size,
				       uint64_t bit_size)
{
	if (bit_field_size && encoding != DRGN_OBJECT_ENCODING_SIGNED &&
	    encoding != DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "bit field must be integer");
	}
	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		if (bit_size == 0 || bit_size > 64) {
			return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
						 "unsupported integer bit size (%" PRIu64 ")",
						 bit_size);
		}
		return NULL;
	case DRGN_OBJECT_ENCODING_FLOAT:
		if (bit_size != 32 && bit_size != 64) {
			return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
						 "unsupported floating-point bit size (%" PRIu64 ")",
						 bit_size);
		}
		return NULL;
	default:
		return NULL;
	}
}

static void drgn_value_deserialize(union drgn_value *value, const void *buf,
				   uint8_t bit_offset,
				   enum drgn_object_encoding encoding,
				   uint64_t bit_size, bool little_endian)
{
	union {
		int64_t svalue;
		uint64_t uvalue;
		double fvalue64;
		float fvalue32;
	} tmp;

	tmp.uvalue = deserialize_bits(buf, bit_offset, bit_size, little_endian);
	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
		value->svalue = sign_extend(tmp.svalue, bit_size);
		break;
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		value->uvalue = tmp.uvalue;
		break;
	case DRGN_OBJECT_ENCODING_FLOAT:
		value->fvalue = bit_size == 32 ? tmp.fvalue32 : tmp.fvalue64;
		break;
	default:
		UNREACHABLE();
	}
}

struct drgn_error *
drgn_byte_order_to_little_endian(struct drgn_program *prog,
				 enum drgn_byte_order byte_order, bool *ret)
{
	SWITCH_ENUM_DEFAULT(byte_order,
	case DRGN_BIG_ENDIAN:
		*ret = false;
		return NULL;
	case DRGN_LITTLE_ENDIAN:
		*ret = true;
		return NULL;
	case DRGN_PROGRAM_ENDIAN:
		return drgn_program_is_little_endian(prog, ret);
	default:
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "invalid byte order");
	)
}

static void copy_bits(void *dst, const void *src, unsigned int bit_offset,
		      uint64_t bit_size, bool little_endian)
{
	unsigned char *d = dst;
	const unsigned char *s = src;
	size_t bytes = bit_size / CHAR_BIT;
	unsigned int bits = bit_size % CHAR_BIT;
	if (little_endian) {
		if (bit_offset) {
			for (size_t i = 0; i < bytes; i++) {
				d[i] = ((s[i] >> bit_offset) |
					(s[i + 1] << (CHAR_BIT - bit_offset)));
			}
		} else if (d != s) {
			memcpy(d, s, bytes);
		}
		if (bits) {
			unsigned char c = s[bytes] >> bit_offset;
			if (bits > CHAR_BIT - bit_offset)
				c |= s[bytes + 1] << (CHAR_BIT - bit_offset);
			d[bytes] = c & ((1U << bits) - 1);
		}
	} else {
		if (bit_offset) {
			for (size_t i = 0; i < bytes; i++) {
				d[i] = ((s[i] << bit_offset) |
					(s[i + 1] >> (CHAR_BIT - bit_offset)));
			}
		} else if (d != s) {
			memcpy(d, s, bytes);
		}
		if (bits) {
			unsigned char c = s[bytes] << bit_offset;
			if (bits > CHAR_BIT - bit_offset)
				c |= s[bytes + 1] >> (CHAR_BIT - bit_offset);
			d[bytes] = c & (-1U << (CHAR_BIT - bits));
		}
	}
}

struct drgn_error *
drgn_object_set_from_buffer_internal(struct drgn_object *res,
				     const struct drgn_object_type *type,
				     enum drgn_object_encoding encoding,
				     uint64_t bit_size, const void *buf,
				     uint64_t bit_offset, bool little_endian)
{
	struct drgn_error *err;

	if (!drgn_object_encoding_is_complete(encoding)) {
		return drgn_error_incomplete_type("cannot create object with %s type",
						  type->type);
	}

	err = sanity_check_object(encoding, type->bit_field_size, bit_size);
	if (err)
		return err;

	const char *p = (const char *)buf + (bit_offset / CHAR_BIT);
	bit_offset %= CHAR_BIT;
	if (encoding == DRGN_OBJECT_ENCODING_BUFFER) {
		/*
		 * `buf` may point inside of `drgn_object_buffer(res)`, so copy
		 * to a temporary value before freeing or modifying the latter.
		 */
		union drgn_value value;

		uint64_t size = drgn_value_size(bit_size);
		char *dst;
		if (size <= sizeof(res->value.ibuf)) {
			dst = value.ibuf;
		} else {
			dst = malloc64(size);
			if (!dst)
				return &drgn_enomem;
			value.bufp = dst;
		}
		copy_bits(dst, p, bit_offset, bit_size, little_endian);

		drgn_object_reinit(res, type, DRGN_OBJECT_ENCODING_BUFFER,
				   bit_size, DRGN_OBJECT_VALUE);
		res->value = value;
		res->little_endian = little_endian;
	} else {
		drgn_object_reinit(res, type, encoding, bit_size,
				   DRGN_OBJECT_VALUE);
		drgn_value_deserialize(&res->value, p, bit_offset, encoding,
				       bit_size, little_endian);
	}
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_from_buffer(struct drgn_object *res,
			    struct drgn_qualified_type qualified_type,
			    const void *buf, size_t buf_size,
			    uint64_t bit_offset, uint64_t bit_field_size,
			    enum drgn_byte_order byte_order)
{
	struct drgn_error *err;

	bool little_endian;
	err = drgn_byte_order_to_little_endian(drgn_object_program(res),
					       byte_order, &little_endian);
	if (err)
		return err;

	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;

	if (bit_size > UINT64_MAX - bit_offset ||
	    buf_size < drgn_value_size(bit_offset + bit_size)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "buffer is too small");
	}

	return drgn_object_set_from_buffer_internal(res, &type, encoding,
						    bit_size, buf, bit_offset,
						    little_endian);
}

static struct drgn_error *
drgn_object_set_reference_internal(struct drgn_object *res,
				   const struct drgn_object_type *type,
				   enum drgn_object_encoding encoding,
				   uint64_t bit_size, uint64_t address,
				   uint64_t bit_offset, bool little_endian)
{
	bool is_64_bit;
	struct drgn_error *err =
		drgn_program_is_64_bit(drgn_object_program(res), &is_64_bit);
	if (err)
		return err;

	err = sanity_check_object(encoding, type->bit_field_size, bit_size);
	if (err)
		return err;

	address += bit_offset / 8;
	address &= is_64_bit ? UINT64_MAX : UINT32_MAX;
	bit_offset %= 8;
	if (bit_size > UINT64_MAX - bit_offset) {
		return drgn_error_format(DRGN_ERROR_OVERFLOW,
					 "object is too large");
	}

	drgn_object_reinit(res, type, encoding, bit_size,
			   DRGN_OBJECT_REFERENCE);
	res->address = address;
	res->bit_offset = bit_offset;
	res->little_endian = little_endian;
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_reference(struct drgn_object *res,
			  struct drgn_qualified_type qualified_type,
			  uint64_t address, uint64_t bit_offset,
			  uint64_t bit_field_size,
			  enum drgn_byte_order byte_order)
{
	struct drgn_error *err;
	bool little_endian;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_byte_order_to_little_endian(drgn_object_program(res),
					       byte_order, &little_endian);
	if (err)
		return err;

	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;
	return drgn_object_set_reference_internal(res, &type, encoding, bit_size,
						  address, bit_offset,
						  little_endian);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_set_absent(struct drgn_object *res,
		       struct drgn_qualified_type qualified_type,
		       uint64_t bit_field_size)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;
	err = sanity_check_object(encoding, type.bit_field_size, bit_size);
	if (err)
		return err;
	drgn_object_reinit(res, &type, encoding, bit_size,
			   DRGN_OBJECT_ABSENT);
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_copy(struct drgn_object *res, const struct drgn_object *obj)
{
	if (res == obj)
		return NULL;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE:
		if (obj->encoding == DRGN_OBJECT_ENCODING_BUFFER) {
			size_t size = drgn_object_size(obj);
			char *dst;
			const char *src;
			if (size <= sizeof(obj->value.ibuf)) {
				dst = res->value.ibuf;
				src = obj->value.ibuf;
			} else {
				dst = malloc(size);
				if (!dst)
					return &drgn_enomem;
				src = obj->value.bufp;
			}
			drgn_object_reinit_copy(res, obj);
			res->kind = DRGN_OBJECT_VALUE;
			memcpy(dst, src, size);
			if (dst != res->value.ibuf)
				res->value.bufp = dst;
			res->little_endian = obj->little_endian;
		} else {
			drgn_object_reinit_copy(res, obj);
			res->kind = DRGN_OBJECT_VALUE;
			res->value = obj->value;
		}
		break;
	case DRGN_OBJECT_REFERENCE:
		drgn_object_reinit_copy(res, obj);
		res->kind = DRGN_OBJECT_REFERENCE;
		res->address = obj->address;
		res->bit_offset = obj->bit_offset;
		res->little_endian = obj->little_endian;
		break;
	case DRGN_OBJECT_ABSENT:
		drgn_object_reinit_copy(res, obj);
		res->kind = DRGN_OBJECT_ABSENT;
		break;
	)
	return NULL;
}

static struct drgn_error *
drgn_object_slice_internal(struct drgn_object *res,
			   const struct drgn_object *obj,
			   struct drgn_object_type *type,
			   enum drgn_object_encoding encoding,
			   uint64_t bit_size, uint64_t bit_offset)
{
	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE: {
		if (obj->encoding != DRGN_OBJECT_ENCODING_BUFFER) {
			return drgn_error_create(DRGN_ERROR_TYPE,
						 "not a buffer object");
		}

		uint64_t bit_end;
		if (__builtin_add_overflow(bit_offset, bit_size, &bit_end) ||
		    bit_end > obj->bit_size) {
			return drgn_error_create(DRGN_ERROR_OUT_OF_BOUNDS,
						 "out of bounds of value");
		}
		return drgn_object_set_from_buffer_internal(res, type, encoding,
							    bit_size,
							    drgn_object_buffer(obj),
							    bit_offset,
							    obj->little_endian);
	}
	case DRGN_OBJECT_REFERENCE:
		if (obj->encoding != DRGN_OBJECT_ENCODING_BUFFER &&
		    obj->encoding != DRGN_OBJECT_ENCODING_INCOMPLETE_BUFFER) {
			return drgn_error_create(DRGN_ERROR_TYPE,
						 "not a buffer object");
		}

		return drgn_object_set_reference_internal(res, type, encoding,
							  bit_size,
							  obj->address,
							  bit_offset,
							  obj->little_endian);
	case DRGN_OBJECT_ABSENT:
		return &drgn_error_object_absent;
	)
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_slice(struct drgn_object *res, const struct drgn_object *obj,
		  struct drgn_qualified_type qualified_type,
		  uint64_t bit_offset, uint64_t bit_field_size)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	err = drgn_object_set_common(qualified_type, bit_field_size, &type,
				     &encoding, &bit_size);
	if (err)
		return err;
	return drgn_object_slice_internal(res, obj, &type, encoding, bit_size,
					  bit_offset);
}

struct drgn_error *
drgn_object_dereference_offset(struct drgn_object *res,
			       const struct drgn_object *obj,
			       struct drgn_qualified_type qualified_type,
			       int64_t bit_offset, uint64_t bit_field_size)
{
	struct drgn_error *err;
	uint64_t address;

	err = drgn_object_read_unsigned(obj, &address);
	if (err)
		return err;

	/*
	 * / and % truncate towards 0. Here, we want to truncate towards
	 * negative infinity. We can accomplish that by replacing "/ 8" with an
	 * arithmetic shift ">> 3" and "% 8" with "& 7".
	 */
	address += bit_offset >> 3;
	bit_offset &= 7;
	return drgn_object_set_reference(res, qualified_type, address,
					 bit_offset, bit_field_size,
					 DRGN_PROGRAM_ENDIAN);
}

static struct drgn_error *
drgn_object_read_reference(const struct drgn_object *obj,
				union drgn_value *value)
{
	struct drgn_error *err;

	assert(obj->kind == DRGN_OBJECT_REFERENCE);

	if (!drgn_object_encoding_is_complete(obj->encoding)) {
		return drgn_error_incomplete_type("cannot read object with %s type",
						  obj->type);
	}

	uint64_t bit_size = obj->bit_size;
	uint8_t bit_offset = obj->bit_offset;
	uint64_t read_size;
	if (bit_offset == 0)
		read_size = drgn_object_size(obj);
	else
		read_size = drgn_value_size(bit_offset + bit_size);

	if (obj->encoding == DRGN_OBJECT_ENCODING_BUFFER) {
		char ibuf_offset[sizeof(value->ibuf) + 1];
		char *buf, *read_buf;
		if (read_size <= sizeof(value->ibuf)) {
			buf = read_buf = value->ibuf;
		} else if (drgn_object_is_inline(obj)) {
			/*
			 * The value fits inside of the inline buffer, but it is
			 * offset, so we need to read an additional byte. Read
			 * it into an on-stack buffer first.
			 */
			buf = value->ibuf;
			read_buf = ibuf_offset;
		} else {
			buf = read_buf = malloc64(read_size);
			if (!buf)
				return &drgn_enomem;
		}
		err = drgn_memory_reader_read(&drgn_object_program(obj)->reader,
					      read_buf, obj->address, read_size,
					      false);
		if (err) {
			if (buf != value->ibuf)
				free(buf);
			return err;
		}
		copy_bits(buf, read_buf, bit_offset, bit_size,
			  obj->little_endian);
		if (buf != value->ibuf)
			value->bufp = buf;
		return NULL;
	} else {
		char buf[9];
		assert(read_size <= sizeof(buf));
		err = drgn_memory_reader_read(&drgn_object_program(obj)->reader,
					      buf, obj->address, read_size,
					      false);
		if (err)
			return err;
		drgn_value_deserialize(value, buf, bit_offset, obj->encoding,
				       bit_size, obj->little_endian);
		return NULL;
	}
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read(struct drgn_object *res, const struct drgn_object *obj)
{
	struct drgn_error *err;

	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE:
		return drgn_object_copy(res, obj);
	case DRGN_OBJECT_REFERENCE: {
		union drgn_value value;

		if (drgn_object_program(res) != drgn_object_program(obj)) {
			return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
						 "objects are from different programs");
		}

		err = drgn_object_read_reference(obj, &value);
		if (err)
			return err;
		drgn_object_reinit_copy(res, obj);
		res->kind = DRGN_OBJECT_VALUE;
		res->value = value;
		res->little_endian = obj->little_endian;
		return NULL;
	}
	case DRGN_OBJECT_ABSENT:
		return &drgn_error_object_absent;
	)
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_value(const struct drgn_object *obj, union drgn_value *value,
		       const union drgn_value **ret)
{
	struct drgn_error *err;

	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE:
		*ret = &obj->value;
		return NULL;
	case DRGN_OBJECT_REFERENCE:
		err = drgn_object_read_reference(obj, value);
		if (!err)
			*ret = value;
		return err;
	case DRGN_OBJECT_ABSENT:
		return &drgn_error_object_absent;
	)
}

static struct drgn_error *
drgn_object_value_signed(const struct drgn_object *obj, int64_t *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	assert(obj->encoding == DRGN_OBJECT_ENCODING_SIGNED);

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	*ret = value->svalue;
	drgn_object_deinit_value(obj, value);
	return err;
}

static struct drgn_error *
drgn_object_value_unsigned(const struct drgn_object *obj, uint64_t *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	assert(obj->encoding == DRGN_OBJECT_ENCODING_UNSIGNED);

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	*ret = value->uvalue;
	drgn_object_deinit_value(obj, value);
	return err;
}

static struct drgn_error *
drgn_object_value_float(const struct drgn_object *obj, double *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	assert(obj->encoding == DRGN_OBJECT_ENCODING_FLOAT);

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	*ret = value->fvalue;
	drgn_object_deinit_value(obj, value);
	return err;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_signed(const struct drgn_object *obj, int64_t *ret)
{
	if (obj->encoding != DRGN_OBJECT_ENCODING_SIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not a signed integer");
	}
	return drgn_object_value_signed(obj, ret);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_unsigned(const struct drgn_object *obj, uint64_t *ret)
{
	if (obj->encoding != DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not an unsigned integer");
	}
	return drgn_object_value_unsigned(obj, ret);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_integer(const struct drgn_object *obj, union drgn_value *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	if (obj->encoding != DRGN_OBJECT_ENCODING_SIGNED &&
	    obj->encoding != DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not an integer");
	}
	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	*ret = *value;
	drgn_object_deinit_value(obj, value);
	return NULL;
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_float(const struct drgn_object *obj, double *ret)
{
	if (obj->encoding != DRGN_OBJECT_ENCODING_FLOAT) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "not floating-point");
	}
	return drgn_object_value_float(obj, ret);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_read_c_string(const struct drgn_object *obj, char **ret)
{
	struct drgn_error *err;
	struct drgn_type *underlying_type;
	uint64_t address;
	size_t max_size;

	underlying_type = drgn_underlying_type(obj->type);
	switch (drgn_type_kind(underlying_type)) {
	case DRGN_TYPE_POINTER:
		err = drgn_object_value_unsigned(obj, &address);
		if (err)
			return err;
		max_size = SIZE_MAX;
		break;
	case DRGN_TYPE_ARRAY:
		if (drgn_type_is_complete(underlying_type)) {
			uint64_t size;

			err = drgn_type_sizeof(underlying_type, &size);
			if (err)
				return err;
			max_size = min(size, (uint64_t)SIZE_MAX);
		} else {
			max_size = SIZE_MAX;
		}
		SWITCH_ENUM(obj->kind,
		case DRGN_OBJECT_VALUE: {
			const char *buf;
			uint64_t value_size;
			size_t len;
			char *p, *str;

			buf = drgn_object_buffer(obj);
			value_size = drgn_object_size(obj);
			len = min(value_size, (uint64_t)max_size);
			p = memchr(buf, 0, len);
			if (p)
				len = p - buf;
			str = malloc(len + 1);
			if (!str)
				return &drgn_enomem;
			memcpy(str, buf, len);
			str[len] = '\0';
			*ret = str;
			return NULL;
		}
		case DRGN_OBJECT_REFERENCE:
			address = obj->address;
			break;
		case DRGN_OBJECT_ABSENT:
			return &drgn_error_object_absent;
		)
		break;
	default:
		return drgn_type_error("string() argument must be an array or pointer, not '%s'",
				       obj->type);
	}

	return drgn_program_read_c_string(drgn_object_program(obj), address,
					  false, max_size, ret);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_format_object(const struct drgn_object *obj, size_t columns,
		   enum drgn_format_object_flags flags, char **ret)
{
	const struct drgn_language *lang = drgn_object_language(obj);

	if (flags & ~DRGN_FORMAT_OBJECT_VALID_FLAGS) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "invalid format object flags");
	}
	return lang->format_object(obj, columns, flags, ret);
}

static struct drgn_error *
drgn_object_convert_signed(const struct drgn_object *obj, uint64_t bit_size,
			   int64_t *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	switch (obj->encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		*ret = truncate_signed(value->svalue, bit_size);
		break;
	case DRGN_OBJECT_ENCODING_FLOAT:
		*ret = truncate_signed(value->fvalue, bit_size);
		break;
	default:
		err = drgn_error_create(DRGN_ERROR_TYPE,
					"object cannot be converted to integer");
		break;
	}
	drgn_object_deinit_value(obj, value);
	return err;
}

static struct drgn_error *
drgn_object_convert_unsigned(const struct drgn_object *obj, uint64_t bit_size,
			     uint64_t *ret)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	switch (obj->encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		*ret = truncate_unsigned(value->uvalue, bit_size);
		break;
	case DRGN_OBJECT_ENCODING_FLOAT:
		*ret = truncate_unsigned(value->fvalue, bit_size);
		break;
	default:
		err = drgn_error_create(DRGN_ERROR_TYPE,
					"object cannot be converted to integer");
		break;
	}
	drgn_object_deinit_value(obj, value);
	return err;
}

static struct drgn_error *
drgn_object_convert_float(const struct drgn_object *obj, double *fvalue)
{
	struct drgn_error *err;
	union drgn_value value_mem;
	const union drgn_value *value;

	err = drgn_object_read_value(obj, &value_mem, &value);
	if (err)
		return err;
	switch (obj->encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
		*fvalue = value->svalue;
		break;
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		*fvalue = value->uvalue;
		break;
	case DRGN_OBJECT_ENCODING_FLOAT:
		*fvalue = value->fvalue;
		break;
	default:
		err = drgn_error_create(DRGN_ERROR_TYPE,
					"object cannot be converted to floating-point");
		break;
	}
	drgn_object_deinit_value(obj, value);
	return err;
}

static struct drgn_error *
drgn_object_is_zero_impl(const struct drgn_object *obj, bool *ret);

static struct drgn_error *
drgn_compound_object_is_zero(const struct drgn_object *obj,
			     struct drgn_type *underlying_type, bool *ret)
{
	struct drgn_error *err;
	struct drgn_object member;
	struct drgn_type_member *members;
	size_t num_members, i;

	drgn_object_init(&member, drgn_object_program(obj));
	members = drgn_type_members(underlying_type);
	num_members = drgn_type_num_members(underlying_type);
	for (i = 0; i < num_members; i++) {
		struct drgn_qualified_type member_type;
		uint64_t member_bit_field_size;
		err = drgn_member_type(&members[i], &member_type,
				       &member_bit_field_size);
		if (err)
			goto out;

		err = drgn_object_slice(&member, obj, member_type,
					members[i].bit_offset,
					member_bit_field_size);
		if (err)
			goto out;

		err = drgn_object_is_zero_impl(&member, ret);
		if (err || !*ret)
			goto out;
	}

	err = NULL;
out:
	drgn_object_deinit(&member);
	return err;
}

static struct drgn_error *
drgn_array_object_is_zero(const struct drgn_object *obj,
			  struct drgn_type *underlying_type, bool *ret)
{
	struct drgn_error *err;
	struct drgn_qualified_type element_type;
	uint64_t element_bit_size, length, i;
	struct drgn_object element;

	element_type = drgn_type_type(underlying_type);
	err = drgn_type_bit_size(element_type.type, &element_bit_size);
	if (err)
		return err;

	drgn_object_init(&element, drgn_object_program(obj));
	length = drgn_type_length(underlying_type);
	for (i = 0; i < length; i++) {
		err = drgn_object_slice(&element, obj, element_type,
					i * element_bit_size, 0);
		if (err)
			goto out;

		err = drgn_object_is_zero_impl(&element, ret);
		if (err || !*ret)
			goto out;
	}

	err = NULL;
out:
	drgn_object_deinit(&element);
	return err;
}

static struct drgn_error *
drgn_object_is_zero_impl(const struct drgn_object *obj, bool *ret)
{
	struct drgn_error *err;

	switch (obj->encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t svalue;

		err = drgn_object_value_signed(obj, &svalue);
		if (err)
			return err;
		if (svalue)
			*ret = false;
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t uvalue;

		err = drgn_object_value_unsigned(obj, &uvalue);
		if (err)
			return err;
		if (uvalue)
			*ret = false;
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_FLOAT: {
		double fvalue;

		err = drgn_object_value_float(obj, &fvalue);
		if (err)
			return err;
		if (fvalue)
			*ret = false;
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_BUFFER: {
		struct drgn_type *underlying_type;

		underlying_type = drgn_underlying_type(obj->type);
		switch (drgn_type_kind(underlying_type)) {
		case DRGN_TYPE_STRUCT:
		case DRGN_TYPE_UNION:
		case DRGN_TYPE_CLASS:
			return drgn_compound_object_is_zero(obj,
							    underlying_type,
							    ret);
		case DRGN_TYPE_ARRAY:
			return drgn_array_object_is_zero(obj, underlying_type,
							 ret);
		default:
			break;
		}
		/* fallthrough */
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "object cannot be converted to boolean");
	}
}

struct drgn_error *drgn_object_is_zero(const struct drgn_object *obj, bool *ret)
{
	*ret = true;
	return drgn_object_is_zero_impl(obj, ret);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_cast(struct drgn_object *res,
		 struct drgn_qualified_type qualified_type,
		 const struct drgn_object *obj)
{
	const struct drgn_language *lang = drgn_type_language(qualified_type.type);

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}
	return lang->op_cast(res, qualified_type, obj);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_reinterpret(struct drgn_object *res,
			struct drgn_qualified_type qualified_type,
			enum drgn_byte_order byte_order,
			const struct drgn_object *obj)
{
	struct drgn_error *err;
	bool little_endian;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	err = drgn_byte_order_to_little_endian(drgn_object_program(res),
					       byte_order, &little_endian);
	if (err)
		return err;

	err = drgn_object_set_common(qualified_type, 0, &type, &encoding,
				     &bit_size);
	if (err)
		return err;

	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE:
		if (obj->encoding != DRGN_OBJECT_ENCODING_BUFFER) {
			return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
						 "cannot reinterpret primitive value");
		}
		err = drgn_object_slice_internal(res, obj, &type, encoding,
						 bit_size, 0);
		if (err)
			return err;
		res->little_endian = little_endian;
		return NULL;
	case DRGN_OBJECT_REFERENCE:
		drgn_object_reinit(res, &type, encoding, bit_size,
				   DRGN_OBJECT_REFERENCE);
		res->address = obj->address;
		res->bit_offset = obj->bit_offset;
		res->little_endian = little_endian;
		return NULL;
	case DRGN_OBJECT_ABSENT:
		return &drgn_error_object_absent;
	)
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_integer_literal(struct drgn_object *res, uint64_t uvalue)
{
	const struct drgn_language *lang =
		drgn_program_language(drgn_object_program(res));
	return lang->integer_literal(res, uvalue);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_bool_literal(struct drgn_object *res, bool bvalue)
{
	const struct drgn_language *lang =
		drgn_program_language(drgn_object_program(res));
	return lang->bool_literal(res, bvalue);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_float_literal(struct drgn_object *res, double fvalue)
{
	const struct drgn_language *lang =
		drgn_program_language(drgn_object_program(res));
	return lang->float_literal(res, fvalue);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_bool(const struct drgn_object *obj, bool *ret)
{
	const struct drgn_language *lang = drgn_object_language(obj);

	return lang->op_bool(obj, ret);
}

LIBDRGN_PUBLIC struct drgn_error *drgn_object_cmp(const struct drgn_object *lhs,
						  const struct drgn_object *rhs,
						  int *ret)
{
	const struct drgn_language *lang = drgn_object_language(lhs);
	if (drgn_object_program(lhs) != drgn_object_program(rhs)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}
	return lang->op_cmp(lhs, rhs, ret);
}

struct drgn_error *drgn_error_binary_op(const char *op_name,
					struct drgn_object_type *lhs_type,
					struct drgn_object_type *rhs_type)
{
	struct drgn_error *err;
	struct drgn_qualified_type lhs_qualified_type = {
		.type = lhs_type->type,
		.qualifiers = lhs_type->qualifiers,
	};
	struct drgn_qualified_type rhs_qualified_type = {
		.type = rhs_type->type,
		.qualifiers = rhs_type->qualifiers,
	};
	char *lhs_type_name, *rhs_type_name;

	err = drgn_format_type_name(lhs_qualified_type, &lhs_type_name);
	if (err)
		return err;
	err = drgn_format_type_name(rhs_qualified_type, &rhs_type_name);
	if (err) {
		free(lhs_type_name);
		return err;
	}
	err = drgn_error_format(DRGN_ERROR_TYPE,
				"invalid operands to %s ('%s' and '%s')",
				op_name, lhs_type_name, rhs_type_name);
	free(rhs_type_name);
	free(lhs_type_name);
	return err;

}

struct drgn_error *drgn_error_unary_op(const char *op_name,
				       struct drgn_object_type *type)
{
	struct drgn_error *err;
	struct drgn_qualified_type qualified_type = {
		.type = type->type,
		.qualifiers = type->qualifiers,
	};
	char *type_name;

	err = drgn_format_type_name(qualified_type, &type_name);
	if (err)
		return err;
	err = drgn_error_format(DRGN_ERROR_TYPE,
				"invalid operand to %s ('%s')",
				op_name, type_name);
	free(type_name);
	return err;
}

#define BINARY_OP(op_name)							\
LIBDRGN_PUBLIC struct drgn_error *						\
drgn_object_##op_name(struct drgn_object *res, const struct drgn_object *lhs,	\
		      const struct drgn_object *rhs)				\
{										\
	const struct drgn_language *lang = drgn_object_language(lhs);		\
										\
	if (drgn_object_program(lhs) != drgn_object_program(res) ||		\
	    drgn_object_program(rhs) != drgn_object_program(res)) {		\
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,		\
					 "objects are from different programs");\
	}									\
	if (!lang->op_##op_name) {						\
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,		\
					 "%s does not implement " #op_name,	\
					 lang->name);				\
	}									\
	return lang->op_##op_name(res, lhs, rhs);				\
}
BINARY_OP(add)
BINARY_OP(sub)
BINARY_OP(mul)
BINARY_OP(div)
BINARY_OP(mod)
BINARY_OP(lshift)
BINARY_OP(rshift)
BINARY_OP(and)
BINARY_OP(or)
BINARY_OP(xor)
#undef BINARY_OP

#define UNARY_OP(op_name)							\
LIBDRGN_PUBLIC struct drgn_error *						\
drgn_object_##op_name(struct drgn_object *res, const struct drgn_object *obj)	\
{										\
	const struct drgn_language *lang = drgn_object_language(obj);		\
										\
	if (drgn_object_program(res) != drgn_object_program(obj)) {		\
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,		\
					 "objects are from different programs");\
	}									\
	if (!lang->op_##op_name) {						\
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,		\
					 "%s does not implement " #op_name,	\
					 lang->name);				\
	}									\
	return lang->op_##op_name(res, obj);					\
}
UNARY_OP(pos)
UNARY_OP(neg)
UNARY_OP(not)
#undef UNARY_OP

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_address_of(struct drgn_object *res, const struct drgn_object *obj)
{
	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	SWITCH_ENUM(obj->kind,
	case DRGN_OBJECT_VALUE:
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
					 "cannot take address of value");
	case DRGN_OBJECT_REFERENCE:
		break;
	case DRGN_OBJECT_ABSENT:
		return &drgn_error_object_absent;
	)

	if (obj->is_bit_field || obj->bit_offset) {
		return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
					 "cannot take address of bit field");
	}

	struct drgn_qualified_type qualified_type =
		drgn_object_qualified_type(obj);
	uint8_t word_size;
	struct drgn_error *err =
		drgn_program_word_size(drgn_object_program(obj), &word_size);
	if (err)
		return err;
	struct drgn_qualified_type result_type;
	err = drgn_pointer_type_create(drgn_object_program(obj), qualified_type,
				       word_size,
				       drgn_type_language(qualified_type.type),
				       &result_type.type);
	if (err)
		return err;
	result_type.qualifiers = 0;
	return drgn_object_set_unsigned(res, result_type,
					obj->address, 0);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_subscript(struct drgn_object *res, const struct drgn_object *obj,
		      int64_t index)
{
	struct drgn_error *err;
	struct drgn_element_info element;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	err = drgn_program_element_info(drgn_object_program(obj), obj->type,
					&element);
	if (err)
		return err;

	if (obj->encoding == DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_object_dereference_offset(res, obj,
						      element.qualified_type,
						      index * element.bit_size,
						      0);
	} else {
		return drgn_object_slice(res, obj, element.qualified_type,
					 index * element.bit_size, 0);
	}
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_member(struct drgn_object *res, const struct drgn_object *obj,
		   const char *member_name)
{
	struct drgn_error *err;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	struct drgn_type_member *member;
	uint64_t member_bit_offset;
	err = drgn_type_find_member(obj->type, member_name, &member,
				    &member_bit_offset);
	if (err)
		return err;
	struct drgn_qualified_type member_type;
	uint64_t member_bit_field_size;
	err = drgn_member_type(member, &member_type, &member_bit_field_size);
	if (err)
		return err;
	return drgn_object_slice(res, obj, member_type, member_bit_offset,
				 member_bit_field_size);
}

struct drgn_error *drgn_object_member_dereference(struct drgn_object *res,
						  const struct drgn_object *obj,
						  const char *member_name)
{
	struct drgn_error *err;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	struct drgn_type *underlying_type = drgn_underlying_type(obj->type);
	if (drgn_type_kind(underlying_type) != DRGN_TYPE_POINTER) {
		return drgn_type_error("'%s' is not a pointer to a structure, union, or class",
				       obj->type);
	}

	struct drgn_type_member *member;
	uint64_t member_bit_offset;
	err = drgn_type_find_member(drgn_type_type(underlying_type).type,
				    member_name, &member, &member_bit_offset);
	if (err)
		return err;
	struct drgn_qualified_type member_type;
	uint64_t member_bit_field_size;
	err = drgn_member_type(member, &member_type, &member_bit_field_size);
	if (err)
		return err;
	return drgn_object_dereference_offset(res, obj, member_type,
					      member_bit_offset,
					      member_bit_field_size);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_container_of(struct drgn_object *res, const struct drgn_object *obj,
			 struct drgn_qualified_type qualified_type,
			 const char *member_designator)
{
	struct drgn_error *err;

	if (drgn_object_program(res) != drgn_object_program(obj)) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "objects are from different programs");
	}

	if (drgn_type_kind(drgn_underlying_type(obj->type)) !=
	    DRGN_TYPE_POINTER) {
		return drgn_type_error("container_of() argument must be a pointer, not '%s'",
				       obj->type);
	}

	uint64_t offset;
	err = drgn_type_offsetof(qualified_type.type, member_designator,
				 &offset);
	if (err)
		return err;

	uint64_t address;
	err = drgn_object_value_unsigned(obj, &address);
	if (err)
		return err;

	uint8_t word_size;
	err = drgn_program_word_size(drgn_object_program(obj), &word_size);
	if (err)
		return err;
	struct drgn_qualified_type result_type;
	err = drgn_pointer_type_create(drgn_object_program(obj), qualified_type,
				       word_size,
				       drgn_type_language(qualified_type.type),
				       &result_type.type);
	if (err)
		return err;
	result_type.qualifiers = 0;
	return drgn_object_set_unsigned(res, result_type, address - offset, 0);
}

LIBDRGN_PUBLIC struct drgn_error *
drgn_object_sizeof(const struct drgn_object *obj, uint64_t *ret)
{
	if (obj->is_bit_field) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "cannot get size of bit field");
	}
	return drgn_type_sizeof(obj->type, ret);
}

static inline struct drgn_error *
binary_operands_signed(const struct drgn_object *lhs,
		       const struct drgn_object *rhs, uint64_t bit_size,
		       int64_t *lhs_ret, int64_t *rhs_ret)
{
	struct drgn_error *err;

	err = drgn_object_convert_signed(lhs, bit_size, lhs_ret);
	if (err)
		return err;
	return drgn_object_convert_signed(rhs, bit_size, rhs_ret);
}

static inline struct drgn_error *
binary_operands_unsigned(const struct drgn_object *lhs,
			 const struct drgn_object *rhs, uint64_t bit_size,
			 uint64_t *lhs_ret, uint64_t *rhs_ret)
{
	struct drgn_error *err;

	err = drgn_object_convert_unsigned(lhs, bit_size, lhs_ret);
	if (err)
		return err;
	return drgn_object_convert_unsigned(rhs, bit_size, rhs_ret);
}

static inline struct drgn_error *
binary_operands_float(const struct drgn_object *lhs,
		      const struct drgn_object *rhs, double *lhs_ret,
		      double *rhs_ret)
{
	struct drgn_error *err;

	err = drgn_object_convert_float(lhs, lhs_ret);
	if (err)
		return err;
	return drgn_object_convert_float(rhs, rhs_ret);
}

static struct drgn_error *pointer_operand(const struct drgn_object *ptr,
					  uint64_t *ret)
{
	switch (ptr->encoding) {
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		return drgn_object_value_unsigned(ptr, ret);
	case DRGN_OBJECT_ENCODING_BUFFER:
	case DRGN_OBJECT_ENCODING_NONE:
	case DRGN_OBJECT_ENCODING_INCOMPLETE_BUFFER:
		SWITCH_ENUM(ptr->kind,
		case DRGN_OBJECT_VALUE:
			return drgn_error_format(DRGN_ERROR_INVALID_ARGUMENT,
						 "cannot get address of value");
		case DRGN_OBJECT_REFERENCE:
			*ret = ptr->address;
			return NULL;
		case DRGN_OBJECT_ABSENT:
			return &drgn_error_object_absent;
		)
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid operand type for pointer arithmetic");
	}
}

static struct drgn_error *drgn_error_cast(struct drgn_object_type *to,
					  struct drgn_object_type *from)
{
	struct drgn_error *err;
	struct drgn_qualified_type to_qualified_type = {
		.type = to->type,
		.qualifiers = to->qualifiers,
	};
	struct drgn_qualified_type from_qualified_type = {
		.type = from->type,
		.qualifiers = from->qualifiers,
	};
	char *to_type_name, *from_type_name;

	err = drgn_format_type_name(to_qualified_type, &to_type_name);
	if (err) {
		return err;
	}
	err = drgn_format_type_name(from_qualified_type, &from_type_name);
	if (err) {
		free(from_type_name);
		return err;
	}
	err = drgn_error_format(DRGN_ERROR_TYPE,
				"cannot convert '%s' to '%s'",
				from_type_name, to_type_name);
	free(from_type_name);
	free(to_type_name);
	return err;
}

struct drgn_error *drgn_op_cast(struct drgn_object *res,
				struct drgn_qualified_type qualified_type,
				const struct drgn_object *obj,
				struct drgn_object_type *obj_type)
{
	struct drgn_error *err;
	struct drgn_object_type type;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	bool is_pointer;

	err = drgn_object_set_common(qualified_type, 0, &type, &encoding,
				     &bit_size);
	if (err)
		goto err;

	if (!drgn_object_encoding_is_complete(encoding)) {
		return drgn_error_incomplete_type("cannot cast to %s type",
						  type.type);
	}

	is_pointer = (drgn_type_kind(obj_type->underlying_type) ==
		      DRGN_TYPE_POINTER);
	switch (encoding) {
	case DRGN_OBJECT_ENCODING_BUFFER: {
		char *type_name;
		err = drgn_format_type_name(qualified_type, &type_name);
		if (err)
			return err;
		err = drgn_error_format(DRGN_ERROR_TYPE, "cannot cast to '%s'",
					type_name);
		free(type_name);
		return err;
	}
	case DRGN_OBJECT_ENCODING_SIGNED: {
		union {
			int64_t svalue;
			uint64_t uvalue;
		} tmp;

		if (is_pointer) {
			err = pointer_operand(obj, &tmp.uvalue);
		} else {
			err = drgn_object_convert_signed(obj, bit_size,
							 &tmp.svalue);
		}
		if (err)
			goto err;
		return drgn_object_set_signed_internal(res, &type, bit_size,
						       tmp.svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t uvalue;

		if (is_pointer) {
			err = pointer_operand(obj, &uvalue);
		} else {
			err = drgn_object_convert_unsigned(obj, bit_size,
							   &uvalue);
		}
		if (err)
			goto err;
		return drgn_object_set_unsigned_internal(res, &type, bit_size,
							 uvalue);
	}
	case DRGN_OBJECT_ENCODING_FLOAT: {
		double fvalue;

		if (is_pointer)
			goto type_error;

		err = drgn_object_convert_float(obj, &fvalue);
		if (err)
			goto err;
		return drgn_object_set_float_internal(res, &type, bit_size,
						      fvalue);
	}
	default:
		goto type_error;
	}

err:
	if (err->code == DRGN_ERROR_TYPE) {
		drgn_error_destroy(err);
		goto type_error;
	}
	return err;

type_error:
	return drgn_error_cast(&type, obj_type);
}

/*
 * Two's complement operator. Avoid undefined/implementation-defined behavior
 * (due to overflow or signed integer representation) for an arithmetic or
 * bitwise operator by doing the operation on unsigned operands and then
 * converting back to a signed integer.
 */
#define BINARY_OP_SIGNED_2C(res, type, bit_size, lhs, op, rhs) ({		\
	struct drgn_error *_err;						\
	uint64_t _bit_size = (bit_size);					\
	union {									\
		int64_t svalue;							\
		uint64_t uvalue;						\
	} lhs_tmp, rhs_tmp, tmp;						\
										\
	_err = binary_operands_signed((lhs), (rhs),  _bit_size,			\
				      &lhs_tmp.svalue, &rhs_tmp.svalue);	\
	if (!_err) {								\
		tmp.uvalue = lhs_tmp.uvalue op rhs_tmp.uvalue;			\
		_err = drgn_object_set_signed_internal((res), (type),		\
						       _bit_size, tmp.svalue);	\
	}									\
	_err;									\
})

#define BINARY_OP_UNSIGNED(res, type, bit_size, lhs, op, rhs) ({		\
	struct drgn_error *_err;						\
	uint64_t _bit_size = (bit_size);					\
	uint64_t lhs_uvalue, rhs_uvalue;					\
										\
	_err = binary_operands_unsigned((lhs), (rhs), _bit_size, &lhs_uvalue,	\
					&rhs_uvalue);				\
	if (!_err) {								\
		_err = drgn_object_set_unsigned_internal((res), (type),		\
							 _bit_size,		\
							 lhs_uvalue op		\
							 rhs_uvalue);		\
	}									\
	_err;									\
})

#define BINARY_OP_FLOAT(res, type, bit_size, lhs, op, rhs) ({			\
	struct drgn_error *_err;						\
	double lhs_fvalue, rhs_fvalue;						\
										\
	_err = binary_operands_float((lhs), (rhs), &lhs_fvalue, &rhs_fvalue);	\
	if (!_err) {								\
		_err = drgn_object_set_float_internal((res), (type),		\
						      (bit_size),		\
						      lhs_fvalue op		\
						      rhs_fvalue);		\
	}									\
	_err;									\
})

#define CMP(lhs, rhs) ({				\
	__auto_type _lhs = (lhs);			\
	__auto_type _rhs = (rhs);			\
							\
	(_lhs > _rhs ? 1 : _lhs < _rhs ? -1 : 0);	\
})

struct drgn_error *drgn_op_cmp_impl(const struct drgn_object *lhs,
				    const struct drgn_object *rhs,
				    const struct drgn_object_type *type,
				    int *ret)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t lhs_svalue, rhs_svalue;

		err = binary_operands_signed(lhs, rhs, bit_size, &lhs_svalue,
					     &rhs_svalue);
		if (err)
			return err;
		*ret = CMP(lhs_svalue, rhs_svalue);
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t lhs_uvalue, rhs_uvalue;

		err = binary_operands_unsigned(lhs, rhs, bit_size, &lhs_uvalue,
					       &rhs_uvalue);
		if (err)
			return err;
		*ret = CMP(lhs_uvalue, rhs_uvalue);
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_FLOAT: {
		double lhs_fvalue, rhs_fvalue;

		err = binary_operands_float(lhs, rhs, &lhs_fvalue, &rhs_fvalue);
		if (err)
			return err;
		*ret = CMP(lhs_fvalue, rhs_fvalue);
		return NULL;
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid operand type for cmp");
	}
}

struct drgn_error *drgn_op_cmp_pointers(const struct drgn_object *lhs,
					const struct drgn_object *rhs, int *ret)
{
	struct drgn_error *err;
	uint64_t lhs_value, rhs_value;

	err = pointer_operand(lhs, &lhs_value);
	if (err)
		return err;
	err = pointer_operand(rhs, &rhs_value);
	if (err)
		return err;

	*ret = CMP(lhs_value, rhs_value);
	return NULL;
}

#undef CMP

#define ARITHMETIC_BINARY_OP(op_name, op)					\
struct drgn_error *								\
drgn_op_##op_name##_impl(struct drgn_object *res,				\
			 const struct drgn_object_type *type,			\
			 const struct drgn_object *lhs,				\
			 const struct drgn_object *rhs)				\
{										\
	struct drgn_error *err;							\
	enum drgn_object_encoding encoding;					\
	uint64_t bit_size;							\
										\
	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);	\
	if (err)								\
		return err;							\
										\
	switch (encoding) {							\
	case DRGN_OBJECT_ENCODING_SIGNED:					\
		return BINARY_OP_SIGNED_2C(res, type, bit_size, lhs, op, rhs);	\
	case DRGN_OBJECT_ENCODING_UNSIGNED:					\
		return BINARY_OP_UNSIGNED(res, type, bit_size, lhs, op, rhs);	\
	case DRGN_OBJECT_ENCODING_FLOAT:					\
		return BINARY_OP_FLOAT(res, type, bit_size, lhs, op, rhs);	\
	default:								\
		return drgn_error_create(DRGN_ERROR_TYPE,			\
					 "invalid result type for " #op_name);	\
	}									\
}
ARITHMETIC_BINARY_OP(add, +)
ARITHMETIC_BINARY_OP(sub, -)
#undef ARITHMETIC_BINARY_OP

struct drgn_error *drgn_op_add_to_pointer(struct drgn_object *res,
					  const struct drgn_object_type *type,
					  uint64_t referenced_size, bool negate,
					  const struct drgn_object *ptr,
					  const struct drgn_object *index)
{
	struct drgn_error *err;
	uint64_t ptr_value, index_value;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;
	if (encoding != DRGN_OBJECT_ENCODING_UNSIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for pointer arithmetic");
	}

	err = pointer_operand(ptr, &ptr_value);
	if (err)
		return err;

	switch (index->encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t svalue;

		err = drgn_object_value_signed(index, &svalue);
		if (err)
			return err;
		if (svalue >= 0) {
			index_value = svalue;
		} else {
			index_value = -svalue;
			negate = !negate;
		}
		break;
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		err = drgn_object_value_unsigned(index, &index_value);
		if (err)
			return err;
		break;
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid addend type for pointer arithmetic");
	}

	if (negate)
		ptr_value -= index_value * referenced_size;
	else
		ptr_value += index_value * referenced_size;
	return drgn_object_set_unsigned_internal(res, type, bit_size,
						 ptr_value);
}

struct drgn_error *drgn_op_sub_pointers(struct drgn_object *res,
					const struct drgn_object_type *type,
					uint64_t referenced_size,
					const struct drgn_object *lhs,
					const struct drgn_object *rhs)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	uint64_t lhs_value, rhs_value;
	int64_t diff;

	if (!referenced_size) {
		return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
					 "object size must not be zero");
	}

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;
	if (encoding != DRGN_OBJECT_ENCODING_SIGNED) {
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for pointer subtraction");
	}

	err = pointer_operand(lhs, &lhs_value);
	if (err)
		return err;
	err = pointer_operand(rhs, &rhs_value);
	if (err)
		return err;

	if (lhs_value >= rhs_value)
		diff = (lhs_value - rhs_value) / referenced_size;
	else
		diff = -((rhs_value - lhs_value) / referenced_size);
	return drgn_object_set_signed_internal(res, type, bit_size, diff);
}

struct drgn_error *drgn_op_mul_impl(struct drgn_object *res,
				    const struct drgn_object_type *type,
				    const struct drgn_object *lhs,
				    const struct drgn_object *rhs)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t lhs_svalue, rhs_svalue;
		uint64_t lhs_uvalue, rhs_uvalue;
		bool lhs_negative, rhs_negative;
		union {
			int64_t svalue;
			uint64_t uvalue;
		} tmp;

		err = binary_operands_signed(lhs, rhs, bit_size,
					     &lhs_svalue, &rhs_svalue);
		if (err)
			return err;

		/*
		 * Convert to sign and magnitude to avoid signed integer
		 * overflow.
		 */
		lhs_negative = lhs_svalue < 0;
		lhs_uvalue = lhs_negative ? -lhs_svalue : lhs_svalue;
		rhs_negative = rhs_svalue < 0;
		rhs_uvalue = rhs_negative ? -rhs_svalue : rhs_svalue;
		tmp.uvalue = lhs_uvalue * rhs_uvalue;
		if (lhs_negative ^ rhs_negative)
			tmp.uvalue = -tmp.uvalue;
		return drgn_object_set_signed_internal(res, type, bit_size,
						       tmp.svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		return BINARY_OP_UNSIGNED(res, type, bit_size, lhs, *, rhs);
	case DRGN_OBJECT_ENCODING_FLOAT:
		return BINARY_OP_FLOAT(res, type, bit_size, lhs, *, rhs);
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for mul");
	}
}

static struct drgn_error drgn_zero_division = {
	.code = DRGN_ERROR_ZERO_DIVISION,
	.message = "division by zero",
};

struct drgn_error *drgn_op_div_impl(struct drgn_object *res,
				    const struct drgn_object_type *type,
				    const struct drgn_object *lhs,
				    const struct drgn_object *rhs)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t lhs_svalue, rhs_svalue;

		err = binary_operands_signed(lhs, rhs, bit_size,
					     &lhs_svalue, &rhs_svalue);
		if (err)
			return err;
		if (!rhs_svalue)
			return &drgn_zero_division;
		return drgn_object_set_signed_internal(res, type, bit_size,
						       lhs_svalue / rhs_svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t lhs_uvalue, rhs_uvalue;

		err = binary_operands_unsigned(lhs, rhs, bit_size, &lhs_uvalue,
					       &rhs_uvalue);
		if (err)
			return err;
		if (!rhs_uvalue)
			return &drgn_zero_division;
		return drgn_object_set_unsigned_internal(res, type, bit_size,
							 lhs_uvalue /
							 rhs_uvalue);
	}
	case DRGN_OBJECT_ENCODING_FLOAT: {
		double lhs_fvalue, rhs_fvalue;

		err = binary_operands_float(lhs, rhs, &lhs_fvalue, &rhs_fvalue);
		if (err)
			return err;
		if (!rhs_fvalue)
			return &drgn_zero_division;
		return drgn_object_set_float_internal(res, type, bit_size,
						      lhs_fvalue / rhs_fvalue);
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for div");
	}
}

struct drgn_error *drgn_op_mod_impl(struct drgn_object *res,
				    const struct drgn_object_type *type,
				    const struct drgn_object *lhs,
				    const struct drgn_object *rhs)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t lhs_svalue, rhs_svalue;

		err = binary_operands_signed(lhs, rhs, bit_size,
					     &lhs_svalue, &rhs_svalue);
		if (err)
			return err;
		if (!rhs_svalue)
			return &drgn_zero_division;
		return drgn_object_set_signed_internal(res, type, bit_size,
						       lhs_svalue % rhs_svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t lhs_uvalue, rhs_uvalue;

		err = binary_operands_unsigned(lhs, rhs, bit_size,
					       &lhs_uvalue, &rhs_uvalue);
		if (err)
			return err;
		if (!rhs_uvalue)
			return &drgn_zero_division;
		return drgn_object_set_unsigned_internal(res, type, bit_size,
							 lhs_uvalue %
							 rhs_uvalue);
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for mod");
	}
}

static struct drgn_error *shift_operand(const struct drgn_object *rhs,
					const struct drgn_object_type *rhs_type,
					uint64_t *ret)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(rhs_type, &encoding,
						 &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t rhs_svalue;

		err = drgn_object_convert_signed(rhs, bit_size, &rhs_svalue);
		if (err)
			return err;
		if (rhs_svalue < 0) {
			return drgn_error_create(DRGN_ERROR_INVALID_ARGUMENT,
						 "negative shift count");
		}
		*ret = rhs_svalue;
		return NULL;
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		return drgn_object_convert_unsigned(rhs, bit_size, ret);
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid rhs type for shift");
	}
}

struct drgn_error *drgn_op_lshift_impl(struct drgn_object *res,
				       const struct drgn_object *lhs,
				       const struct drgn_object_type *lhs_type,
				       const struct drgn_object *rhs,
				       const struct drgn_object_type *rhs_type)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	uint64_t shift;

	err = drgn_object_type_encoding_and_size(lhs_type, &encoding,
						 &bit_size);
	if (err)
		return err;

	err = shift_operand(rhs, rhs_type, &shift);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		union {
			int64_t svalue;
			uint64_t uvalue;
		} tmp;

		err = drgn_object_convert_signed(lhs, bit_size, &tmp.svalue);
		if (err)
			return err;
		/* Left shift of a negative integer is undefined. */
		if (shift < bit_size)
			tmp.uvalue <<= shift;
		else
			tmp.uvalue = 0;
		return drgn_object_set_signed_internal(res, lhs_type, bit_size,
						       tmp.svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t uvalue;

		err = drgn_object_convert_unsigned(lhs, bit_size, &uvalue);
		if (err)
			return err;
		if (shift < bit_size)
			uvalue <<= shift;
		else
			uvalue = 0;
		return drgn_object_set_unsigned_internal(res, lhs_type,
							 bit_size, uvalue);
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for lshift");
	}
}

struct drgn_error *drgn_op_rshift_impl(struct drgn_object *res,
				       const struct drgn_object *lhs,
				       const struct drgn_object_type *lhs_type,
				       const struct drgn_object *rhs,
				       const struct drgn_object_type *rhs_type)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;
	uint64_t shift;

	err = drgn_object_type_encoding_and_size(lhs_type, &encoding,
						 &bit_size);
	if (err)
		return err;

	err = shift_operand(rhs, rhs_type, &shift);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED: {
		int64_t svalue;

		err = drgn_object_convert_signed(lhs, bit_size, &svalue);
		if (err)
			return err;
		if (shift < bit_size)
			svalue >>= shift;
		else if (svalue >= 0)
			svalue = 0;
		else
			svalue = -1;
		return drgn_object_set_signed_internal(res, lhs_type, bit_size,
						       svalue);
	}
	case DRGN_OBJECT_ENCODING_UNSIGNED: {
		uint64_t uvalue;

		err = drgn_object_convert_unsigned(lhs, bit_size, &uvalue);
		if (err)
			return err;
		if (shift < bit_size)
			uvalue >>= shift;
		else
			uvalue = 0;
		return drgn_object_set_unsigned_internal(res, lhs_type,
							 bit_size, uvalue);
	}
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for lshift");
	}
}

#define INTEGER_BINARY_OP(op_name, op)						\
struct drgn_error *								\
drgn_op_##op_name##_impl(struct drgn_object *res,				\
			 const struct drgn_object_type *type,			\
			 const struct drgn_object *lhs,				\
			 const struct drgn_object *rhs)				\
{										\
	struct drgn_error *err;							\
	enum drgn_object_encoding encoding;					\
	uint64_t bit_size;							\
										\
	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);	\
	if (err)								\
		return err;							\
										\
	switch (encoding) {							\
	case DRGN_OBJECT_ENCODING_SIGNED:					\
		return BINARY_OP_SIGNED_2C(res, type, bit_size, lhs, op, rhs);	\
	case DRGN_OBJECT_ENCODING_UNSIGNED:					\
		return BINARY_OP_UNSIGNED(res, type, bit_size, lhs, op, rhs);	\
	default:								\
		return drgn_error_create(DRGN_ERROR_TYPE,			\
					 "invalid result type for " #op_name);	\
	}									\
}
INTEGER_BINARY_OP(and, &)
INTEGER_BINARY_OP(or, |)
INTEGER_BINARY_OP(xor, ^)
#undef INTEGER_BINARY_OP

/* See BINARY_OP_SIGNED_2C. */
#define UNARY_OP_SIGNED_2C(res, type, bit_size, op, obj) ({			\
	struct drgn_error *_err;						\
	uint64_t _bit_size = (bit_size);					\
	union {									\
		int64_t svalue;							\
		uint64_t uvalue;						\
	} tmp;									\
										\
	_err = drgn_object_convert_signed((obj), _bit_size, &tmp.svalue);	\
	tmp.uvalue = op tmp.uvalue;						\
	if (!_err) {								\
		_err = drgn_object_set_signed_internal((res), (type),		\
						       _bit_size,		\
						       tmp.svalue);		\
	}									\
	_err;									\
})

#define UNARY_OP_UNSIGNED(res, type, bit_size, op, obj) ({			\
	struct drgn_error *_err;						\
	uint64_t _bit_size = (bit_size);					\
	uint64_t uvalue;							\
										\
	_err = drgn_object_convert_unsigned((obj), bit_size, &uvalue);		\
	if (!_err) {								\
		_err = drgn_object_set_unsigned_internal((res), (type),		\
							 _bit_size, op uvalue);	\
										\
	}									\
	_err;									\
})

#define ARITHMETIC_UNARY_OP(op_name, op)					\
struct drgn_error *								\
drgn_op_##op_name##_impl(struct drgn_object *res,				\
			 const struct drgn_object_type *type,			\
			 const struct drgn_object *obj)				\
{										\
	struct drgn_error *err;							\
	enum drgn_object_encoding encoding;					\
	uint64_t bit_size;							\
										\
	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);	\
	if (err)								\
		return err;							\
										\
	switch (encoding) {							\
	case DRGN_OBJECT_ENCODING_SIGNED:					\
		return UNARY_OP_SIGNED_2C(res, type, bit_size, op, obj);	\
	case DRGN_OBJECT_ENCODING_UNSIGNED:					\
		return UNARY_OP_UNSIGNED(res, type, bit_size, op, obj);		\
	case DRGN_OBJECT_ENCODING_FLOAT: {					\
		double fvalue;							\
										\
		err = drgn_object_convert_float(obj, &fvalue);			\
		if (err)							\
			return err;						\
		return drgn_object_set_float_internal(res, type, bit_size,	\
						      op fvalue);		\
										\
	}									\
	default:								\
		return drgn_error_create(DRGN_ERROR_TYPE,			\
					 "invalid result type for " #op_name);	\
	}									\
}
ARITHMETIC_UNARY_OP(pos, +)
ARITHMETIC_UNARY_OP(neg, -)
#undef ARITHMETIC_UNARY_OP

struct drgn_error *drgn_op_not_impl(struct drgn_object *res,
				    const struct drgn_object_type *type,
				    const struct drgn_object *obj)
{
	struct drgn_error *err;
	enum drgn_object_encoding encoding;
	uint64_t bit_size;

	err = drgn_object_type_encoding_and_size(type, &encoding, &bit_size);
	if (err)
		return err;

	switch (encoding) {
	case DRGN_OBJECT_ENCODING_SIGNED:
		return UNARY_OP_SIGNED_2C(res, type, bit_size, ~, obj);
	case DRGN_OBJECT_ENCODING_UNSIGNED:
		return UNARY_OP_UNSIGNED(res, type, bit_size, ~, obj);
	default:
		return drgn_error_create(DRGN_ERROR_TYPE,
					 "invalid result type for not");
	}
}
