const toastLiveExample = document.getElementById('liveToast')

if (toastLiveExample) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
  console.log('toastBootstrap');
  toastBootstrap.show()
}