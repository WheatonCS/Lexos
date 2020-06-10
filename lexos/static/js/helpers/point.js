/**
 * Gets the sum of two point-like objects.
 * @param {{x, y}} a The first addend.
 * @param {{x, y}} b The second addend.
 * @returns {{x: number, y: number}} The product of a and b.
 */
function point_add (a, b) {
  return {x: a.x + b.x, y: a.y + b.y}
}

/**
 * Gets the difference of two point-like objects.
 * @param {{x, y}} a The minuend.
 * @param {{x, y}} b The subtrahend.
 * @returns {{x: number, y: number}} The difference of a and b.
 */
function point_subtract (a, b) {
  return {x: a.x - b.x, y: a.y - b.y}
}

/**
 * Gets the minimum of two point-like objects.
 * @param {{x, y}} a The first point.
 * @param {{x, y}} b The second point.
 * @returns {{x: number, y: number}} The minimum of a and b.
 */
function point_minimum (a, b) {
  return {x: Math.min(a.x, b.x), y: Math.min(a.y, b.y)}
}

/**
 * Gets the maximum of two point-like objects.
 * @param {{x, y}} a The first point.
 * @param {{x, y}} b The second point.
 * @returns {{x: number, y: number}} The maximum of a and b.
 */
function point_maximum (a, b) {
  return {x: Math.max(a.x, b.x), y: Math.max(a.y, b.y)}
}
