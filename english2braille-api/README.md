# About

This API was created for Recess Hacks 2023 for use alongside [cocacolachicken/backend-server-e2braille](https://www.github.com/cocacolachicken/backend-server-e2braille). 

A common misconception surrounding Braille is that it is simply a one-to-one correspondance with letters of the English alphabet. While that is more or less true for Grade 1 Braille, Grade 2 Braille presents great difficulty in translation and difficulty. This API uses Flask and wraps an algorithm (painstakingly written by [@Abby012](https://github.com/Abby012)) for translating English writing to Grade 1 and Grade 2 Braille.

# API specifications

Both of these algorithms assume that the punctuation and capitalization are correct (as deviations are rather trivial in the case of translating to Braille.)

## POST /translate

``{
  'translate' : '{your text here}'
}``

Returns a grade 2 Braille translation of the specified 'translate'.

## POST /translate1

``{
  'translate' : '{your text here}'
}``

Returns a grade 1 Braille translation of the specified 'translate'.
