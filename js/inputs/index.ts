import { Radio } from './radio';
import { input, InputFunction } from './input';

export const CUSTOM_INPUTS: Record<string, InputFunction> = {
    radio: options => input(Radio, options),
};
