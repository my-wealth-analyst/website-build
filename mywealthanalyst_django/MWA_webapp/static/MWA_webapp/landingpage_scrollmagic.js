$(document).ready(function(){

// Init ScrollMagic
var controller = new ScrollMagic.Controller();

// pin the intro
var pinIntroScene = new ScrollMagic.Scene({
      triggerElement: "#intro",
      triggerHook: 0,
      duration: '40%',
})
.setPin('#intro', {pushFollowers: true})
.addIndicators()
.addTo(controller)

var Scene1_pic = new ScrollMagic.Scene({
      triggerElement: "#Dashboard_Mobile1",
      triggerHook: "100%",
})
.setClassToggle('#Dashboard_Mobile1', 'Dashboard_Mobile1_end' )
.addIndicators()
.addTo(controller)


// loop through each .scroll_frame element
$('.scroll_frame img').each(function(){
  // Build Scene1
  var Scene1 = new ScrollMagic.Scene({
      triggerElement: this,
      triggerHook: 0.6,
      reverse: false,
  })
  .setClassToggle(this, 'zero-position') // add class to
  .addIndicators()
  .addTo(controller);

});


});
