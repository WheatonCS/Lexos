/**
 * Open graph in fullscreen mode.
 */
function openFullscreen(id='graph-container') {
    let elem = document.getElementById(id)
    document.getElementById('full-screen-button').style.display = 'none'
    if (elem.requestFullscreen) {
        elem.requestFullscreen()
    } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen()
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
        elem.webkitRequestFullscreen()
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen()
    }
  }

/* Close fullscreen */
if (document.addEventListener) {
    document.addEventListener('fullscreenchange', exitHandler, false)
    document.addEventListener('mozfullscreenchange', exitHandler, false)
    document.addEventListener('MSFullscreenChange', exitHandler, false)
    document.addEventListener('webkitfullscreenchange', exitHandler, false)
}

function exitHandler() {
    if (!document.fullscreenElement && !document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
        let btn = document.getElementById('full-screen-button')
        btn.style.display = 'inline-flex'
    }
}
