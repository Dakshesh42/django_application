$(document).ready(function () {
  //jquery for toggle sub menus
  $('.sub-btn').click(function () {
    $(this).next('.sub-menu').slideToggle();
    $(this).find('.dropdown').toggleClass('rotate');
  });
});


$(document).ready( function () {
  $('#table_id').DataTable();
} );

$(document).ready( function () {
  $('#table_id1').DataTable();
} );

$(document).ready( function () {
  $('#table_id2').DataTable();
} );

$(document).ready( function () {
  $('#table_ontime').DataTable();
} );

$(document).ready( function () {
  $('#table_late').DataTable();
} );


$(document).ready( function () {
  $('#table_notcheck').DataTable();
} );

$(document).ready( function () {
  $('#table_absent').DataTable();
} );

$(document).ready( function () {
  $('#table_my-attendance').DataTable();
} );

$(document).ready( function () {
  $('#table_view-prev-task').DataTable();
} );

$(document).ready( function () {
  $('#table_emp-list').DataTable();
} );

$(document).ready( function () {
  $('#table-pdf').DataTable();
} );

$(document).ready( function () {
  $('#table_client-list').DataTable();
} );

$(document).ready( function () {
  $('#table_client-contact').DataTable();
} );
$(document).ready( function () {
  $('#table_ccontact-page').DataTable();
} );
$(document).ready( function () {
  $('#table_attendance-list').DataTable();
} );
$(document).ready( function () {
  $('#table_ips-all').DataTable();
} );
$(document).ready( function () {
  $('#table_project-list').DataTable();
} );
$(document).ready( function () {
  $('#table_resource-list').DataTable();
} );

const projectSelect = $('#res_project');
projectSelect.on('change', function() {
  const projectId = $(this).val();
  console.log("projectId: ",projectId);

  $.ajax({
    url: '/check-project-hours/',
    type: 'GET',
    dataType: 'json',
    data: {
      project_id: projectId,
      csrfmiddlewaretoken: '{{ csrf_token }}'
    },
    success: function(response) {
      console.log(response);
      const remainingHours = response.remaining_hours;
      const remainingMaxHours = response.remaining_max_hours;
      console.log(remainingHours);
      const messageElement = $('#remaining-hours-message');
      if (response) {
        messageElement.html('Remaining Hours : ( Min - ' + remainingHours + ' | Max - ' + remainingMaxHours + ' )');
      } else {
        messageElement.html('The selected project has no remaining hours.');
      }
    },
    error: function(xhr, status, error) {
      // Handle any errors
      console.log(error);
    }
  });
});


//EWS-Tabs
(() => {
  var ewsTabs = document.querySelectorAll("[ews-tab]");
  if (ewsTabs.length > 0) {
    ewsTabs.forEach((tabs) => {
      var tabButtons = tabs.querySelectorAll("[ews-tab-selector]");
      var tabContents = tabs.querySelectorAll("[ews-tab-content]");

      tabButtons[0].classList.add("active");
      tabContents[0].classList.add("active");

      tabButtons.forEach((tabButton) => {
        tabButton.addEventListener("click", () => {
          var tabName = tabButton.getAttribute("ews-tab-selector");
          var tabContent = tabs.querySelector(
            '[ews-tab-content="' + tabName + '"]'
          );

          tabContents.forEach((content) => {
            content.classList.remove("active");
          });

          tabButtons.forEach((button) => {
            button.classList.remove("active");
          });

          tabButton.classList.add("active");
          tabContent.classList.add("active");
        });
      });
    });
  }
})();

// modal

$("a").click(function(){
  $("#popup").fadeToggle( "slow" );
});

