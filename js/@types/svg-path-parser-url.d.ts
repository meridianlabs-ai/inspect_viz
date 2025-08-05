declare module 'https://cdn.jsdelivr.net/npm/svg-path-parser@1.1.0/+esm' {
    function parseSVG(path: string): any[];
    function makeAbsolute(commands: any[]): any[];

    const svgPathParser: {
        (path: string): any[];
        parseSVG: typeof parseSVG;
        makeAbsolute: typeof makeAbsolute;
    };

    export default svgPathParser;
}
