# AI Data Transformers

This repo contains a library that uses LLMs for data transformations on values in Pandas or Spark dataframes.

The core value prop is that the library exposes simple building blocks for writing transformations thta use LLM to perform some computation over the data as given by a prompt. In essence, instead of defining a data transformation logic in detailed code, we replace the logic with an LLM, i.e. we instruct the LLM to take an instruction and process and get the desired output from the data.

For example, consider the problem for needing to parse out the data from raw text which can be in format: unix timestamp, UTC timestamp, textual description, in Japanese etc. Traditionally, data engineers need to write well-test transformation of ever-increasing subsets of cases on highly filtered data to do so. But you can do so with just an LLM call with the instruction: "parse out time and write it out as a UTC timestamp".

The library exposes interfaces for both API-based models and open source models. In particular, once can take a possible quantized model and use that. The library takes care of optimially running it, the worker distribution and serialization.


## Low-Level Functions -> Let Pandas etc. handle it
Map, Reduce, Serialize

## Composition Functions -> Let User Define them
Don't define composition abstractions, let users handle it.

## Text Level Functions

transform(x, transform_instruction)
structify(x, model: PydanticBaseModel, structify_instruction=None)
classify(x, c, labels=[], classification_instruction=None)
score_in_range(x, range_start, range_end, scoring_instruction=None)
extract(x, types=[])


## Optimizations
### Compile Transformations
For a sequence of transformations, if you compile and serialize, under the hood, the models will reuse the KV-cache for the input.