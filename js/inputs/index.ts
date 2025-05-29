import { Radio } from './radio';
import { input, InputFunction } from './input';

// Creating a custom input:
//
// (1) Implement the custom input in js/_input (e.g. see radio.ts)
// (2) Add the custom input to CUSTOM_INPUTS below
// (3) Create a py wrapper with input: <custom> (e.g. see radio.py)

export const CUSTOM_INPUTS: Record<string, InputFunction> = {
    radio: options => input(Radio, options),
};
