login();
// result_data is a file name.
    $.couch.db("数据库名").openDoc("存数据的doc名", {
        // if success, then trigger function (data)
        success: function (data) {
            // 先画一个随着年份改变，发推数量变化的曲线图。
            var echart1=echarts.init(document.getElementById('main2'));
            var cityName=["Sydney","Melbourne","Perth","Brisbane"];
            var senario=["alcohol","profanity","crime","positive",];
            // following items in "" are defined in couchdb before.
            var count= [data["Sydneycount"],data["Melbournecount"],
                data["Perthcount"],data["Brisbanecount"]];
            var alcohol=[data["Sydneycount"]-data["Sydneybeer"],
                data["Melbournecount"]-data["Melbournebeer"],
                data["Perthcount"]- data["Perthbeer"],
                data["Brisbanecount"]-data["Brisbanebeer"]];
            var crime=[data["Sydneycount"]-data["Sydneycrime"],
                data["Melbournecount"]-data["Melbournecrime"],
                data["Perthcount"]-data["Perthcrime"],
                data["Brisbanecount"]-data["Brisbanecrime"]];
            var profanity = [data["Sydneycount"]-data["Sydneyprofanity"],
                data["Melbournecount"]-data["Melbourneprofanity"],
                data["Perthcount"]-data["Perthprofanity"],
                data["Brisbanecount"]-data["Brisbaneprofanity"]];
            var positive=[data["Sydneypositive"],data["Melbournepositive"],
                data["Perthpositive"],data["Brisbanepositive"]];
            var negative=[data["Sydneynegative"],data["Melbournenegative"],
                data["Perthnegative"],data["Brisbanenegative"]];
            var neutral=[data["Sydneyneutral"],data["Melbourneneutral"],
                data["Perthneutral"],data["Brisbaneneutral"]];

            var option1={
                title:{
                    text:'All scenarios',
                },

                legend:{
                    data:["Count","Alcohol","Crime","Profanity","Positive","Neutral","Negative"]
                },
                xAxis:{
                    data:cityName
                },
                yAxis:{
                },
                tooltip:{
                    show:true,
                },
                series:[
                    {
                        name:'Count',
                        type:'bar',
                        data:count,
                        itemStyle: {
                            normal: {
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#1b10ff'
                                    },
                                }
                            }
                        },
                        markLine:{
                                data:[
                                    {type:'average',name:'average',itemStyle:{
                                            normal:{
                                                color:'red'
                                            }
                                        }}
                                ]
                            }
                        },{
                        name:'Alcohol',
                        type:'bar',
                        data:alcohol,
                            itemStyle: {
                                normal: {
                                    label: {
                                        show: true,
                                        position: 'top',
                                        textStyle: {
                                            color: '#ff1715'
                                        },
                                    }}},
                        },{
                            name:'Crime',
                            type:'bar',
                            data:crime,
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: true,
                                            position: 'top',
                                            textStyle: {
                                                color: '#ff0d7c'
                                            },
                                        }}},
                        },{
                            name:'Profanity',
                            type:'bar',
                            data:profanity,
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: true,
                                            position: 'top',
                                            textStyle: {
                                                color: '#14c5ff'
                                            },
                                        }}},
                        },
                            {
                            name:'Positive',
                            type:'bar',
                            data:positive,
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: true,
                                            position: 'top',
                                            textStyle: {
                                                color: '#f8ff11'
                                            },
                                        }}},
                            markLine:{
                                data:[
                                    {type:'average',name:'average',itemStyle:{
                                            normal:{
                                                color:'blue'
                                            }
                                        }}
                                ]
                            }
                        },
                            {
                                name:'Neutral',
                                type:'bar',
                                data:neutral,
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: true,
                                            position: 'top',
                                            textStyle: {
                                                color: '#fb16ff'
                                            },
                                        }}},
                            },{
                                name:'Negative',
                                type:'bar',
                                data:negative,
                                itemStyle: {
                                    normal: {
                                        label: {
                                            show: true,
                                            position: 'top',
                                            textStyle: {
                                                color: '#ff8e0f'
                                            },
                                        }}},
                                markLine:{
                                    data:[
                                        {type:'average',name:'average',itemStyle:{
                                                normal:{
                                                    color:'black'
                                                }
                                            }}
                                    ]
                                }
                            }
                        ]
                };
                echart1.setOption(option1);
            },
            error:function (status) {
                console.log(status);
                alert("Cannot get data from database");
            }
        });