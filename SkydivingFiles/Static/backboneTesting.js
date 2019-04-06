$(function(){

  var Jumper = Backbone.Model.extend({
    defaults: {
      checked: false
    },
    select: function() {
      this.set('checked', !this.get('checked'));
    }
  });

  var JumperList = Backbone.Collection.extend({
    model: Jumper,
    getSelected: function () {
      return this.where({checked:true});
    }
  });

  var jumpers = new JumperList([
    new Jumper({ checked:false, name: 'Griffin'}),
    new Jumper({ checked:true, name: 'James'})
  ]);

  var JumperDisplay = Backbone.View.extend({
    tagName: 'li',
    events: {
      'click': 'toggleSelect'
    },
    initialize: function () {
      //event listeners

      this.listenTo(this.model, 'change', this.render);
    },
    render: function () {
      //create the html
      this.$el.html('<input type="checkbox" value="1" name="' + this.model.get('name') + '">' + this.model.get('name') );
      this.$('input').prop('checked', this.model.get('checked'));
      // good practice to return the object to make chaining possible
      return this;
    },
    toggleSelect: function() {
      this.model.select();
    }
  });

  var App = Backbone.View.extend({

    el: $('#main'),
    initialize: function() {
      this.listenTo(jumpers, 'change', this.render);

      this.list = $('#jumpers');
      this.total = $('#total span');

      //create views for each service
      jumpers.forEach(function(jumper) {
        var view = new JumperDisplay({ model: jumper});
        this.list.append(view.render().el);
      }, this); // this is the context in the callback
    },
    render: function() {
      var total = 0
      _.each(jumpers.getSelected(), function(elm) {
        total += 1;
      });
      this.total.text(total)
      return this;
    }
  });
  new App();
});

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
      var person = new Jumper({name: name});
      $('.jumpers').append("<li>" + person.attributes.name + "</li>")
      //var jumperStr = "<li class='jumper'>" + name + "</li>"
      //$("#activeJumpers").append(jumperStr)
    })
  });
};
