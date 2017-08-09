/* In the Margins Side Panel Functions */
/* Based on https://github.com/AndreaLombardo/BootSideMenu */
/* function getSide(listClasses){
    var side;
    for (var i = 0; i<listClasses.length; i++) {
        if (listClasses[i]=='sidebar-left') {
            side = "left";
            break;
        } else if (listClasses[i]=='sidebar-right') {
            side = "right";
            break;
        } else {
            side = null;
        }
    }
    return side;
}

function doAnimation(container, containerWidth, sidebarSide, sidebarStatus) {
    var toggler = container.children()[1];
    if (sidebarStatus == "opened") {
        if (sidebarSide == "left") {
            container.animate({
                left: -(containerWidth+32)
            });
            toggleArrow("left");
        } else if (sidebarSide == "right") {
            container.animate({
                right: -(containerWidth +2)
            });
            toggleArrow("right");
        }
        container.attr('data-status', 'closed');
    } else {
        if (sidebarSide == "left") {
            container.animate({
                left:0
            });
            toggleArrow("right");
        } else if (sidebarSide == "right") {
            container.animate({
                right:0
            });
            toggleArrow("left");
        }
        container.attr('data-status', 'opened');
    }
}

function toggleArrow(side){
    if (side=="left") {
        $("#toggler").children(".glyphicon-chevron-right").css('display', 'block');
        $("#toggler").children(".glyphicon-chevron-left").css('display', 'none');
    } else if (side=="right") {
        $("#toggler").children(".glyphicon-chevron-left").css('display', 'block');
        $("#toggler").children(".glyphicon-chevron-right").css('display', 'none');
    }
} */

/* Document Ready Functions */
$(document).ready(function () {
  /* ITM Panel Setup */
  /*    var container = $("#toggler").parent();
      var containerWidth = container.width();
      container.css({left:-(containerWidth+32)});
      container.attr('data-status', 'closed'); */

  /* ITM Panel Toggle Events */
  /* Note: This function currently only works with side-panel toggle icon.
     To enable the use of other triggers, a class trigger should be used. */
  $('#cog-toggler').click(function (e) {
    e.preventDefault()
    $('#settings-modal').modal('hide')
    $('#toggler').click()
  })

  $('#toggler').click(function () {
    var container = $(this).parent()
    var listClasses = $(container[0]).attr('class').split(/\s+/) // IE9 Fix
    var side = getSide(listClasses)
    var containerWidth = container.width()
    var status = container.attr('data-status')
    var dataSlug = $('#ITMPanel-itm-content').attr('data-slug')
    var slug = (dataSlug == '') ? 'index' : dataSlug
    if (!status) {
      status = 'closed'
    }
    doAnimation(container, containerWidth, side, status)
    if (status == 'closed') {
      $('#panel-status').show()
      callAPI(slug, 'panel')
    }
  })

  /* Populate a Bootstrap modal */
  $('#ITM-modal').on('show.bs.modal', function (e) {
    var button = $(e.relatedTarget) // Button that triggered the modal
    var slug = button.data('slug') // Extract info from data-slug attribute
    var type = button.data('type') // Extract info from data-type attribute
    $('#dialog-status').show()
    callAPI(slug, type)
    // callAPI("best-practices", "dialog");
  })

  /* Empty a Bootstrap modal */
  $('#ITM-modal').on('hide.bs.modal', function () {
    $('#ITM-modal').removeData('bs.modal')
    icon = $('#dialog-status').parent().html()
    $('#ITM-modal .modal-body').html('')
    $('#ITM-modal .modal-body').html(icon)
    $('#dialog-status').hide()
    callAPI('best-practices', 'dialog')
  })

  /* Handle Show Video Button in Bootstrap Modal */
  /*    $('#show-video').click(function() {
          callAPI("how-to-read-a-dendrogram", "video-dialog")
      }); */
})

/* Initialise Bootstrap Modal */
$('#ITM-modal').modal()
