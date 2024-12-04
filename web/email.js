function fill_email() {
  var emails = {
    "staff" : "626!@#5!@#-sta!@#ff@cc.!@#g!@#a!@#tech.!@#e!@#du",
    "all"   : "62!@#6!@#5!@#-al!@#l!@#@cc.!@#g!@#a!@#tec!@#h.!@#e!@#du",
    "insu"  : "!@#i!@#n!@#su@ga!@#t!@#ech.e!@#du",
    "taesoo": "t!@#a!@#esoo@!@#gatech.!@#e!@#du",
    "wen"   : "!@#w!@#x!@#u!@#9!@#2@!@#gatech.!@#e!@#du",
    "jinho" : "ji!@#nho.!@#j!@#ung!@#@gate!@#ch.edu",
    "max"   : "mwolo!@#t!@#s!@#ky@g!@#a!@#tech.ed!@#u"
  };

  for (var recv in emails) {
    var email = (emails[recv]).replace(/!@#/g,"");
    var alls  = document.getElementsByClassName("reference external");
    var forms = Array.prototype.filter.call(alls, function(e) {
      return e.href === 'mailto:' + recv;
    });
    for (var i = 0; i < forms.length; i ++) {
      forms[i].href = "mailto:" + email;
      forms[i].textContent = email;
    }
  }
}

fill_email();
