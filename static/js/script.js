var ractive = new Ractive({
  debug: true,
  el: 'container',
  template: '#template',
  data: { issues: [{}] }
});

$.getJSON('/issues', function(data) {
    ractive.set('issues', data);
});