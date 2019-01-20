function genLoads() {
  console.log("hello");
  var url = "//localhost:4000/upcomingLoads/";
  $.getJSON(url, function(data) {
    var items = [];
    $.each(data, function(content, load) {
      load.forEach(listJumpers);
    });
  });
};

function listJumpers(load) {
    var loadNum = "<ul class='singleLoad' id='" + load.load +"'> Load Number: " + load.load + "</ul>";
    $(".loads").append(loadNum);
    var jumpers = load.jumpers;
    jumpers.forEach(function printName (jumper) {
      var name = jumper.name;
      var listItem = "<li id='jumper'>" + name + "</li>";
      $("#" + load.load + "").append(listItem);
    });
  };

genLoads();


function orderAry() {
  var url = "//localhost:4000/upcomingLoads/";
  $.getJSON(url, function(data) {
    var loadAry = [];
    console.log("here")
    $.forEach(data, function (content, load) {
      loadAry.push(load);
    });
  });
  loadAry.sort();
  console.log(loadAry);
};
orderAry();
