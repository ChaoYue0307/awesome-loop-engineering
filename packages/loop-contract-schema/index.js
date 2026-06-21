'use strict';

// The canonical schema is copied in at pack time (see prepack in package.json),
// so it is present in the published package.
const schema = require('./loop-contract.schema.json');
const validate = require('./validate');

/**
 * Validate a loop contract object against the Loop Engineering schema.
 * @param {unknown} contract - parsed JSON loop contract
 * @returns {string[]} list of validation errors (empty when valid)
 */
function validateContract(contract) {
  return validate(contract, schema, '$');
}

module.exports = { schema, validate, validateContract };
