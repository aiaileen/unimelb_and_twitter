var results = []
            login()
                // result_data is a file name.
                $.couch.db("result").openDoc("ArtUnimelb", {
                // if success, then trigger function (data)
                    success: function getData(data) {
                        result[0] = data
                    },
                    error: function (status) {
                        console.log(status);
                        alert("Cannot get data from database");
                    }
                })