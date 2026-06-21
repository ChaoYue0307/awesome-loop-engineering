# @chaoyue0307/loop-contract-schema

The machine-readable [Loop Contract](../../README.md#the-loop-contract) schema from [Awesome Loop Engineering](https://github.com/ChaoYue0307/awesome-loop-engineering), packaged with a dependency-free validator.

A loop contract is the portable spec for a recurring AI-agent loop: objective, trigger, intake, workspace, context, agents, verification, state, budget, escalation, and exit. The canonical schema lives at [`schemas/loop-contract.schema.json`](../../schemas/loop-contract.schema.json); this package ships a copy plus a validator so other projects can check their own contracts.

## Install

This package is published to GitHub Packages. Point the scope at the GitHub registry, then install:

```sh
echo "@chaoyue0307:registry=https://npm.pkg.github.com" >> .npmrc
npm install @chaoyue0307/loop-contract-schema
```

## Use as a library

```js
const { schema, validateContract } = require('@chaoyue0307/loop-contract-schema');

const errors = validateContract(myContract);
if (errors.length === 0) {
  console.log('valid loop contract');
} else {
  console.error(errors.join('\n'));
}
```

## Use as a CLI

```sh
npx loop-contract-validate path/to/contract.json
```

Exit code `0` means the contract is valid; `1` means validation errors (printed to stderr); `2` means a usage or read error.

## Notes

- The validator implements only the JSON Schema keywords the contract uses (`type`, `enum`, `minLength`, `minimum`, `minItems`, `items`, `required`, `additionalProperties`, `properties`), so it stays dependency-free. For full JSON Schema validation, use the schema with a standard validator such as Ajv.
- Repository materials are released under CC0-1.0.
