
var social = new Vue({
    el:"#social",
    // data:{

    data () {
    return {
      openSimple: false
    };
  },
  methods: {
    openSimpleDialog () {
      this.openSimple = true;
      $('#qrcode-dialog').css("display","table")

    },
    closeSimpleDialog () {
      this.openSimple = false;
    }
  }
    //
    // }
});
