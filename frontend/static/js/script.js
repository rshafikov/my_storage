const input = document.getElementById('myInput');

input.addEventListener('keyup', function() {
  if (!input.value.startsWith('/')) {
    input.value = '/' + input.value;
  }
});
