'use strict';

// Dependency-free validator for the subset of JSON Schema keywords used by
// loop-contract.schema.json. Mirrors scripts/check_loop_contract_examples.py.

function typeMatches(value, expected) {
  if (expected === 'object') return value !== null && typeof value === 'object' && !Array.isArray(value);
  if (expected === 'array') return Array.isArray(value);
  if (expected === 'string') return typeof value === 'string';
  if (expected === 'integer') return typeof value === 'number' && Number.isInteger(value);
  return true;
}

function validate(value, schema, path) {
  if (path === undefined) path = '$';
  const errors = [];

  const expectedType = schema.type;
  if (typeof expectedType === 'string' && !typeMatches(value, expectedType)) {
    return [`${path}: expected ${expectedType}, got ${Array.isArray(value) ? 'array' : typeof value}`];
  }

  if (Array.isArray(schema.enum) && !schema.enum.includes(value)) {
    errors.push(`${path}: expected one of ${JSON.stringify(schema.enum)}, got ${JSON.stringify(value)}`);
  }

  if (typeof value === 'string' && Number.isInteger(schema.minLength) && value.length < schema.minLength) {
    errors.push(`${path}: string is shorter than ${schema.minLength}`);
  }

  if (typeof value === 'number' && Number.isInteger(value) && Number.isInteger(schema.minimum) && value < schema.minimum) {
    errors.push(`${path}: value is less than ${schema.minimum}`);
  }

  if (Array.isArray(value)) {
    if (Number.isInteger(schema.minItems) && value.length < schema.minItems) {
      errors.push(`${path}: array has fewer than ${schema.minItems} items`);
    }
    if (schema.items && typeof schema.items === 'object') {
      value.forEach((item, index) => {
        errors.push(...validate(item, schema.items, `${path}[${index}]`));
      });
    }
  }

  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    const required = schema.required || [];
    for (const key of required) {
      if (!(key in value)) errors.push(`${path}: missing required key '${key}'`);
    }

    const properties = schema.properties || {};
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(value)) {
        if (!(key in properties)) errors.push(`${path}: unexpected key '${key}'`);
      }
    }

    for (const [key, childSchema] of Object.entries(properties)) {
      if (key in value && childSchema && typeof childSchema === 'object') {
        errors.push(...validate(value[key], childSchema, `${path}.${key}`));
      }
    }
  }

  return errors;
}

module.exports = validate;
