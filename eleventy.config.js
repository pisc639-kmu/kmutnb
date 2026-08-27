const postcss = require("postcss");
const atImport = require("postcss-import");
const tailwindcss = require("@tailwindcss/postcss");
const { transform } = require("lightningcss");
const { minify } = require("terser");
const htmlmin = require("html-minifier-terser");

module.exports = function (eleventyConfig) {
  eleventyConfig.ignores.add("README.md");
  eleventyConfig.ignores.add("src/**");
  eleventyConfig.ignores.add("static/**");
  eleventyConfig.ignores.add("node_modules/**");
  eleventyConfig.ignores.add("old-unused-others/**");
  eleventyConfig.ignores.add("ignore/**");

  eleventyConfig.addPassthroughCopy("**/*.csv");
  eleventyConfig.addPassthroughCopy("images/**");
  eleventyConfig.addPassthroughCopy("schedule/**/*.json");
  eleventyConfig.addPassthroughCopy({ "404.html": "404.html" });
  // eleventyConfig.addPassthroughCopy({ "script.min.js": "script.min.js" });
  // eleventyConfig.addPassthroughCopy({ "old-exam-script.js": "old-exam-script.min.js" });

  eleventyConfig.addTemplateFormats("css");
  eleventyConfig.addExtension("css", {
    outputFileExtension: "min.css", // Generates style.min.css
    compile: async function (inputContent, inputPath) {
      if (inputPath.endsWith(".min.css")) return;

      return async () => {
        const postcssResult = await postcss([
          atImport(),
          tailwindcss(),
        ]).process(inputContent, {
          from: inputPath,
        });

        let { code } = transform({
          code: Buffer.from(postcssResult.css),
          minify: true,
        });

        return code.toString();
      };
    },
  });

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

  // HTML Transform to strip comments & minify inline scripts without mangling names
  eleventyConfig.addTransform("htmlmin", async function (content, outputPath) {
    if (outputPath && outputPath.endsWith(".html")) {
      return await htmlmin.minify(content, {
        removeComments: true,
        collapseWhitespace: true,
        minifyJS: {
          mangle: true, // Keeps original variable and function names
        },
        minifyCSS: function (text) {
          try {
            const { code } = transform({
              code: Buffer.from(text),
              minify: true,
            });
            return code.toString();
          } catch (e) {
            return text; // Fallback if parsing fails
          }
        },
      });
    }
    return content;
  });

  return {
    dir: {
      input: ".",
      output: "_site",
    },
  };
};