order=[];
rscid = '';

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function getdetails(l){
    for(i=0; i<l.length; i++){
        if(l[i]['rscid'] == (document.getElementById('customerslist')).value){
            rscid = l[i]['rscid'];
            if(document.getElementById('yo'))
            {
                rem();
            }
                var a = document.createElement('h5');
                a.setAttribute('id', 'yo');
                var  x = document.createTextNode('Name: '+l[i]['name']);
                a.appendChild(x);
                var b = document.createElement('h5');
                b.setAttribute('id', 'yo');
                var  x = document.createTextNode('Address: '+l[i]['address']);
                b.appendChild(x);
                var c = document.createElement('h5');
                c.setAttribute('id', 'yo');
                var  x = document.createTextNode('Phone: '+l[i]['phone']);
                c.appendChild(x);
                var d = document.createElement('h5');
                d.setAttribute('id', 'yo');
                var  x = document.createTextNode('Shop: '+l[i]['shop']);
                d.appendChild(x);
                var e = document.createElement('h5');
                e.setAttribute('id', 'yo');
                var  x = document.createTextNode('GST: '+l[i]['gst']);
                e.appendChild(x);
                document.getElementById('dtls').appendChild(a);
                document.getElementById('dtls').appendChild(b);
                document.getElementById('dtls').appendChild(c);
                document.getElementById('dtls').appendChild(d);
                document.getElementById('dtls').appendChild(e);
                break;
       }
   }
}
function rem(){
    document.getElementById('yo').remove();
    document.getElementById('yo').remove();
    document.getElementById('yo').remove();
    document.getElementById('yo').remove();
    document.getElementById('yo').remove();
}

function sendit(l){
    var desi = document.getElementById('goodlist').value;
    var qtiy = document.getElementById('quantityid').value;
    var rate = document.getElementById('rateid').value;
    var gstrate = document.getElementById('gstid').value;
    if (gstrate == ''){
        gstrate = 0;
    }
    if(desi==''){
        alert('Please Select the item!');
    }
    else if(qtiy == ''){
        alert('Please fill up Quantity!');
    }
    else if(rate == ''){
        alert('Please fill up Rate!');
    }
    else{
    order[order.length] = {'rsgid':desi, 'quantity':qtiy, 'rate': rate, 'gst': gstrate};
    for(i=0; i<l.length; i++){
        if(desi == l[i]['rsgid']){
            good_name = l[i]['name'];
            break;
        }
    }

    var remover = document.getElementById('goodlist');

    remover.remove(remover.selectedIndex);
    remover.selectedIndex=''

    var row = document.createElement('tr');
    row.setAttribute('id', 'rowid');

    var divdes = document.createElement('td');
        //divdes.setAttribute('class', 'des_class');
        // var des = document.createElement('a');
        // des.setAttribute('id', 'about');
        var  x = document.createTextNode(good_name);
        divdes.appendChild(x);
        //divdes.appendChild(des);
    
    var divqty = document.createElement('td');
        //divqty.setAttribute('class', 'qty_class');
        // var qty = document.createElement('a');
        // qty.setAttribute('id', 'listqtyclass');
        var  x = document.createTextNode(qtiy);
        divqty.appendChild(x);
        //divqty.appendChild(qty);

    var divrate = document.createElement('td');
        //divrate.setAttribute('class', 'rate_class');
        // var ra = document.createElement('a');
        // ra.setAttribute('id', 'listrateclass');
        var  x = document.createTextNode(rate);
        divrate.appendChild(x);
        //divrate.appendChild(ra);

    var divgst = document.createElement('td');
        //divgst.setAttribute('class', 'tot_class');
        // var gst = document.createElement('a');
        // gst.setAttribute('id', 'gstclass');
        var  x = document.createTextNode((gstrate/100)*(rate*qtiy));
        divgst.appendChild(x);
        //divgst.appendChild(gst);

    var divtot = document.createElement('td');
        //divtot.setAttribute('class', 'tot_class');
        // var totl = document.createElement('a');
        // totl.setAttribute('id', 'totlclass');
        var  x = document.createTextNode((rate*qtiy)+((gstrate/100)*(rate*qtiy)));
        divtot.appendChild(x);
        //divtot.appendChild(totl);
   
    

    list = document.getElementById('sublistid').appendChild(row);
    list.insertBefore(divtot, list.childNodes[0]);
    list.insertBefore(divgst, list.childNodes[0]);
    list.insertBefore(divrate, list.childNodes[0]);
    list.insertBefore(divqty, list.childNodes[0]);
    list.insertBefore(divdes, list.childNodes[0]);
    //-----------------------------------------------------------------------------------
    // document.getElementById('rowid').appendChild(divdes);//appended in table.
    // document.getElementById('rowid').appendChild(divqty);
    // document.getElementById('rowid').appendChild(divrate);
    // document.getElementById('rowid').appendChild(divgst);
    // document.getElementById('rowid').appendChild(divtot);
    //-----------------------------------------------------------------------------
    // resets the solumns
    document.getElementById('rateid').value='';
    document.getElementById('quantityid').value='';
    document.getElementById('gstid').value='';
    //also create an json with appender. which append rsgid, qty and rate, gst
}
}

function resets(l){
    var desi = document.getElementById('goodlist').value;
    for(i=0; i<l.length; i++){
        if(desi == l[i]['rsgid']){
            quan = l[i]['quantity'];
            break;
        }
    }
    try{
    document.getElementById('quan_classid').remove();
    }
    catch(err){}
    var divquna = document.createElement('div');
    divquna.setAttribute('id', 'quan_classid')
    var amtt = document.createElement('a');
    var text = document.createTextNode(quan);
    amtt.appendChild(text);
    divquna.appendChild(amtt)
    document.getElementById('quantityshow').appendChild(divquna);
    document.getElementById('rateid').value='';
    document.getElementById('quantityid').value='';
    document.getElementById('gstid').value='0';
}

//also add document.getelementbyid('clickme').click();
function poster(){
    if (rscid==''){
        alert('Select Customer');
    }
    else if (order.length == 0){
        alert("Cart can not be empty!");
    }
    else{
        x = confirm("Proceed to Checkout?");
        if (x == true){
           addi=  document.getElementById('additional').value;
           if(addi == '')
           {
               addi = 0;
           }
        order[order.length]= {'customer_id': rscid, 'transport': document.getElementById('transport').value, 'additional_cost': addi};
        x='';
        for (i=0; i<order.length;i++){
        x += JSON.stringify(order[i])+", ";
        }
        document.getElementById('getme').value = x;
        document.getElementById("clickmeautomatic").click();
        transactionlink =  "http://192.168.1.9:5000/transaction/"+ rscid;
        //window.location.href= transactionlink;
    }
}
}

function disableinp(val, qty){
    var x = document.getElementById(val);
    
    if (x.style.display === "none") {
        x.value = '';
        x.style.display = "block";
      } else {
        x.value = 'done';
        x.style.display = "none";
      }
}

function postit(){
    var ll = document.getElementById('tallytable').getElementsByTagName('td');
    j = [];
    for (i = 0; i<ll.length; i++){
        if(ll[i].className == 'classinput'){
            rsgid = ll[i].getElementsByTagName('input')[0].getAttribute('id');
            console.log(rsgid);
            qty = ll[i].getElementsByTagName('input')[0].value;
            console.log('quantity', qty);
            j[j.length] = {'rsgid': rsgid, 'quantity':qty};
        }
    }
    console.log('here j', j)
    x='';
    for (i=0; i<j.length;i++){
    x += JSON.stringify(j[i])+", ";
    }
    document.getElementById('fillme').value = x;
    console.log(document.getElementById('fillme').value);
    t = confirm('Order will be marked as Done. Continue?')
    if (t == true){
    document.getElementById('clickclak').click();
}
}

function movetotrans(){
    x = document.getElementById('customerslist').value;
    lin = 'http://192.168.1.9:5000/transaction/'+x;
    window.location.href= lin;
}