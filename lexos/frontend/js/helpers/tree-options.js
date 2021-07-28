/**
 * Registers options popup creation callbacks for the "Distance Metric" and
 * "Linkage Method" buttons.
 * @returns {void}
 */
function initialize_tree_options () {
  // Register the "Distance Metric" button callback
  $('#distance-metric-button').click(function () {
    create_radio_options_popup('Distance Metric', 'distance_metric',
      '#distance-metric-button', '#distance-metric-input',

      ['Euclidean', 'Minkowski', 'Manhattan', 'Standard Euclidean',
        'Squared Euclidean', 'Cosine', 'Correlation', 'Hamming',
        'Chebychev', 'Jaccard', 'Canberra', 'Braycurtis'],

      ['euclidean', 'minkowski', 'cityblock', 'seuclidean',
        'sqeuclidean', 'cosine', 'correlation', 'hamming',
        'chebyshev', 'jaccard', 'canberra', 'braycurtis'])
  })

  // Register the "Linkage Method" button callback
  $('#linkage-method-button').click(function () {
    create_radio_options_popup('Linkage Method', 'linkage_method',
      '#linkage-method-button', '#linkage-method-input',

      ['Average', 'Single', 'Complete', 'Weighted'])
  })
  $('#kernel-type-button').click(function () {
    create_radio_options_popup('Kernel Type', 'kernel_type',
      '#kernel-type-button', '#kernel-type-input',

      ['Linear', 'RBF', 'Polynomial', 'Sigmoid'],

      ['linear', 'rbf', 'poly', 'sigmoid'])
  })
}
