$(function(){
  //Jumper model
  var Jumper = Backbone.Model.extend({
    defaults: {
      checked: false
    },
    select: function(){
      this.set('checked', !this.get('checked'));
    }
  });

  // Jumper List Collection
  var JumperList = Backbone.Collection.extend({
    model: Jumper,
    getSelected: function(){
      return this.where({checked:true});
    }
  });

  // This is where we get our list of jumpers
  var jumpers = new JumperList(function(){
    var url = "//localhost:4000/jumpers";
    var ary = [];
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
      jumpers.forEach(function(){
        ary.push(this);
      })
    });


  // Jumper view
  var JumperDisplay = Backbone.View.extend({
    tagname:'li',
    events: {
      'click': 'toggleSelect'
    },
    initialize: function(){
      // event listeners
      this.listenTo(this.model, 'change', this.render)
    },
    render: function(){
      this.$el.html('<input type="checkbox" value="1" name="' + this.model.get('name') + '">' + this.model.get('name') );
      this.$('input').prop('checked', this.model.get('checked'));
      // good practice to return the object to make chaining possible
      return this;
    },
    toggleSelect: function(){
      this.model.select()
    }
  });

  // Now the entire app
  var App = Backbone.View.extend({
    el: $('#main'),
    initialize: function(){
      this.listenTo(jumpers, 'change', this.render);

      this.list = $('#activeJumpers');
      this.total = $('#total')

      jumprs.forEach(function(jumper){
        var view = new JumperDisplay({model:JumperDisplay});
        this.list.append(view.render().el);
      }, this); // this is the context for the callback
    },
    render: function(){
      var total = 0
      _.each(jumpers.getSelected(), function(elm) {
        total += 1;
      });
      this.total.text(total)
      return this;
    }
  });
  new App();
})
