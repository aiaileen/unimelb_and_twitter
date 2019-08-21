function login(){
    $.couch.urlPrefix = "http://45.113.233.247:5984";
    //$.couch.urlPrefix = "http://localhost:5984"
    $.couch.info({
        success: function(data) {
            console.log(data);
        }
    });
    $.couch.login({
        name: "admin",
        password: "admin",
        success: function(data) {
            console.log(data);
        },
        error: function(status) {
            console.log(status);
        }
    });
    }