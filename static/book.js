function updateDate(){
    var now = new Date();

    var date = now.getDate(),
        mth = now.getMonth(),
        year = now.getFullYear(),
        datec1,
        date2,month2,year2,datec2;

    //date = 28;
    //mth = 1;
    //year=2024;
    date = date + 1;
    mth = mth + 1;
    date2 = date - 4;
    month2 = mth + 1;
    year2 = year + 1;

    if(date<5)
        date2 = 1;
    
    if((year%400==0||(year%4==0&&year%100!=0))&&mth==2&&date==30){
        date=1;
        mth=mth+1;
        date2=1;
        month2=month2+1;
    }else if(mth==2&&date==29){
        date=1;
        mth=mth+1;
        date2=1;
        month2=month2+1;
    }

    if(mth==12){
        date2 = date;
        month2 = 1;
        if(date==32){
            date=1;
            mth=1;
            year = year2;
            date2=1;
            month2=2;
        }
    }

    if((mth==1||mth==3||mth==5||mth==7||mth==8||mth==10) && date==32){
        date=1;
        mth=month2;
        date2 = 1;
        month2 = month2 + 1;
    }

    if((mth==4||mth==6||mth==9||mth==11) && date==31){
        date=1;
        mth=month2;
        date2=1;
        month2 = month2 + 1;
        if(mth==12){
            month2 = 1;
        }
    }


    date = date.toString();
    mth = mth.toString();
    date2 = date2.toString();
    month2 = month2.toString();

    if(date.length == 1){
        date = date.padStart(2, "0");
        //alert(date);
    }
    if(mth.length == 1){
        mth = mth.padStart(2, "0");
    }
    if(date2.length == 1){
        date2 = date2.padStart(2, "0");
        //alert(date);
    }
    if(month2.length == 1){
        month2 = month2.padStart(2, "0");
    }

    datec1 = year+"-"+mth+"-"+date;
    datec2 = year+"-"+month2+"-"+date2;

    if(mth==12){
        datec2 = year2+"-"+month2+"-"+date2;
    }

    var ele = document.getElementById("datec");
    ele.setAttribute("min",datec1);
    ele.setAttribute("max",datec2);


    //ele.min = year+"-"+month+"-"+date;

}
function initDate(){
    updateDate();
    window.setInterval("updateDate()",60000);
}

