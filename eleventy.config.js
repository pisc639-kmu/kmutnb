const postcss = require("postcss");
const atImport = require("postcss-import");
const tailwindcss = require("@tailwindcss/postcss");
const { transform } = require("lightningcss");
const { minify } = require("terser");

module.exports = function (eleventyConfig) {
  // 1. Ignore specific files and folders
  eleventyConfig.ignores.add("README.md");
  eleventyConfig.ignores.add("src/**");
  eleventyConfig.ignores.add("static/**");
  eleventyConfig.ignores.add("node_modules/**");
  eleventyConfig.ignores.add("old-unused-others/**");
  eleventyConfig.ignores.add("ignore/**");

  // 2. Passthrough static minified JS
  eleventyConfig.addPassthroughCopy("images/**");
  eleventyConfig.addPassthroughCopy("schedule/**/*.json");
  eleventyConfig.addPassthroughCopy({ "404.html": "404.html" });
  eleventyConfig.addPassthroughCopy({ "script.min.js": "script.min.js" });

  // 3. Process Tailwind CSS v4 + Minify
  eleventyConfig.addTemplateFormats("css");
  eleventyConfig.addExtension("css", {
    outputFileExtension: "min.css", // Generates style.min.css
    compile: async function (inputContent, inputPath) {
      // Skip processing already-minified CSS files
      if (inputPath.endsWith(".min.css")) return;

      return async () => {
        // Step A: Resolve @import "tailwindcss" and build utility classes via PostCSS
        const postcssResult = await postcss([
          atImport(),
          tailwindcss(),
        ]).process(inputContent, {
          from: inputPath,
        });

        // Step B: Minify using LightningCSS
        let { code } = transform({
          code: Buffer.from(postcssResult.css),
          minify: true,
        });

        return code.toString();
      };
    },
  });

  // 4. Process & Minify JS
  eleventyConfig.addTemplateFormats("js");
  eleventyConfig.addExtension("js", {
    outputFileExtension: "min.js",
    compile: async function (inputContent, inputPath) {
      if (inputPath.endsWith(".min.js")) return;
      if (inputPath.endsWith(".config.js")) return;

      return async () => {
        const minified = await minify(inputContent);
        return minified.code;
      };
    },
  });

  // 5. Template Filters
  eleventyConfig.addNunjucksAsyncFilter("jsmin", async function (code, callback) {
    try {
      const minified = await minify(code);
      callback(null, minified.code);
    } catch (err) {
      callback(err);
    }
  });

  eleventyConfig.addFilter("cssmin", function (code) {
    let { code: output } = transform({
      code: Buffer.from(code),
      minify: true,
    });
    return output.toString();
  });

  return {
    dir: {
      input: ".",
      output: "_site",
    },
  };
};