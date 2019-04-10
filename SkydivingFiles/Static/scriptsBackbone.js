'use strict'

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
    url: "//localhost:4000/jumpers",
    getSelected: function(){
      return this.where({checked:true});
    },
    parse: function(response){

      var self = this;
      //console.log(response)
      _.each(response.Jumper, function(jumper, index){
        //console.log(jumper);
        //console.log(index);

        var member  = new self.model();
        member.set('name', jumper.name);

        self.push(member)
      });
      //console.log('length of this collection: ' + this.length);
      //console.log(this.models);

      return this.models;
    }
  });
  // This is where we get our list of jumpers
  var jumpers = new JumperList();
  console.log(jumpers.fetch(jumpers.parse))
  //console.log(jumpers);
  //  new Jumper({ checked:false, name: 'Griffin'}),
  //  new Jumper({ checked:true, name: 'James'})
//])

  // Jumper view
  var JumperDisplay = Backbone.View.extend({
    tagname:'li',
    events: {
      'click': 'toggleSelect'
    },
    initialize: function(){
      // event listeners
      this.listenTo(this.model, 'change', this.render)
      this.collection = new JumperList();
      //console.log(this.collection)

      var self = this;

      this.collection.fetch({
        url: this.collection.url,
        type: 'GET',
        contentType: 'application/json',
        data: JSON.stringify({
          fields:[
            'name'
          ]
        }),
        reset: true,
        // as fetch is asynchronous, wait for it to complete
        success: function(){
          //console.log(this);
        }
      });
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

      jumpers.forEach(function(jumper){
        var view = new JumperDisplay({model:jumper});
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
