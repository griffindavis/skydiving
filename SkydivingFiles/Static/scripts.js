function listLoadFrame(load) {
    var loadNum = "<ul class='singleLoad' id='" + load.load +"'></ul>";
    $(".loadDisplay").append(loadNum);
    loadNum="<li class='loadHeader'>Load: " + load.load + "</li>";
    $('#'+load.load).append(loadNum);
    var jumpers = load.jumpers;
    jumpers.forEach(function printName (jumper) {
      var name = jumper.name;
      var listItem = "<li>" + name + "</li>";
      $("#" + load.load + "").append(listItem);
    });
  };
// what if we ordered backwards?
// wouldn't have to worry about adjusting the starting point
function orderLoads() {
  var url = "//localhost:4000/upcomingLoads/";
  $.getJSON(url, function (data) {
    var loads = data.load;
    loads.sort(function(first, sec) {
      if (first.load > sec.load) {
        return 1
      }
      else if (first.load < sec.load) {
        return -1
      }
      else return 0
    });
    loads.forEach(function printLoad(load) {
      listLoadFrame(load);
    });
  });
};

function loadJumpers() {
  var url = "//localhost:4000/jumpers"
  $.getJSON(url, function (data) {
    var jumpers = data.Jumper;
    jumpers.sort(function(first, sec) {
      if (first.name > sec.name) {
        return 1
      }
      else if (first.name < sec.name) {
        return -1
      }
      else return 0
    });
    jumpers.forEach(function(jumper) {
      var name = jumper.name;
      var jumperStr = "<li class='jumper'>" + name + "</li>"
      $("#activeJumpers").append(jumperStr)
    })
  });
};

orderLoads();
loadJumpers();


$('.jumper').mouseover(function(item) {
  item.stopPropagation();
  $(this).addClass('loadHover');
});

//$('.jumper').onclick(function(item) {
//  var toAdd = $('addToLoad');
//  var newJumper = "<li>add this</li>"
//  $('.addToLoad').appendChild(newJumper)
//});
