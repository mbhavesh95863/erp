function salesTemplatetable_IncrimentRowIdNumber(startPosition, increment) {
    //get all the items with the data-row attr. - this will include tr and td
    var items = $('[data-row]');

    //for each item with a data-row attr. increment the value
    for (i = 0; i < items.length; i++) {
        //get the current value
        var rowNum = parseInt(items.eq(i).attr('data-row'));

        //only update the rows that are after the new inserted row
        if (rowNum >= startPosition) {
            //generate the new value and update the item
            var newId = rowNum + parseInt(increment);
            items.eq(i).attr('data-row', newId);
            items.eq(i).find('.del').attr('onClick', 'salesTemplatetable_DelRow(' + newId + ')');
            items.eq(i).find('.sitems').attr('id', 'sitems' + newId);
        }
    }
}

function AddNewRow2() {
    //using jquery, grab a reference to the html table
    var salesTemplatetable = $('#salesTemplatetable');
    //get the number of rows and columns
    var colCount = salesTemplatetable.find('td[data-row=0]').length;
    var rowCount = $("#salesTemplatetable tr").length;

    row = rowCount - 1;
    //incriment position numbers to make room for the new row
    //this is required to keep things working after we change the table
    salesTemplatetable_IncrimentRowIdNumber(row, 1);

    //add row
    var newRow = '<tr data-row="' + row + '" class="item-row">';
    //add cells into the row
    for (addCol = 0; addCol < colCount; addCol++) {
        if (addCol == 0) {
            newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><a href="javascript:;"  class="del"  onClick=" salesTemplatetable_DelRow(' + row + ')">X</a></td>';
        } else if (addCol == 1) {
            newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><div class="autocomplete"><input type="hidden" class="uom" name="uom" value=""><input type="hidden" class="sitemsid" name="sitemsid" value=""><input type="hidden" class="item_code" name="item_code" value=""><input type="hidden" class="ppk_calculation" name="ppk_calculation" value="0"><input  class="sitems"  id="sitems' + row + '" type="text" name="sitems" value=""></div></td>';
        } else if (addCol == 2) {
            newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><input name="idesc" class="idesc" type="text" value=""></td>';
        } else if (addCol == 3) {
            newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><input type="hidden" class="purchase_pallets"  name="purchase_pallets" value=""><input type="hidden" class="gross_weight"  name="gross_weight" value=""><input type="text" class="weight" name="weight" value=""></td>';
        }
		else {
			if (addCol == (colCount - 1)) {
               newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><span class="ppktotal">0.0</span></td>';
            } else if (addCol == (colCount - 2)) {
                 newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><span class="qtytotal">0.0</span><span class="gwgtitotal">0.0</span></td>';
            }
			else
			{
				newRow += '<td data-row="' + row + '" data-col="' + addCol + '"><input type="hidden" class="iname' + addCol + '" id="iname" name="iname' + addCol + '" value=""><input type="hidden"   id="rqty" name="rqty' + addCol + '" class="rqty' + addCol + '" value="0"><input type="text"   id="iqty" name="iqty' + addCol + '" class="iqty' + addCol + '" value="0"><input  id="iprice"  type="text" class="iprice' + addCol + '" name="iprice' + addCol + '" value="0.0"></td>';
			}
        }
    }
    //close the row
    newRow += '</tr>';
    //add the new row after the previous row in the table - the magic of jquery <img draggable="false" class="emoji" alt="ðŸ™‚" src="https://s.w.org/images/core/emoji/2.4/svg/1f642.svg">
    $(newRow).insertAfter('tr[data-row=' + (parseInt(row) - 1) + ']');
}

function AddNewCol2() {
    var salesTemplatetable = $('#salesTemplatetable');
    var colCount = salesTemplatetable.find('td[data-row=0]').length;
    var rowCount = $("#salesTemplatetable tr").length;

    colNum = colCount - 2;
    //incriment id numbers to make room for the new column
    salesTemplatetable_IncrimentColIdNumber(colNum, 1);

    //add new column by adding a new cell to each row
    for (row = 0; row < rowCount; row++) {
        //add a new cell after the cell for the previous column
        if (row == 0) {
            $('td[data-row=' + row + '][data-col=' + (parseInt(colNum) - 1) + ']').after('<td data-row="' + row + '" data-col="' + colNum + '"><a href="javascript:;" class="delCol" onClick="salesTemplatetable_DelCol(' + colNum + ')">X</a></td>');
        } else if (row == 1) {
            $('td[data-row=' + row + '][data-col=' + (parseInt(colNum) - 1) + ']').after('<td data-row="' + row + '" data-col="' + colNum + '"><input type="hidden" class="isupplierid" name="isupplierid" value=""><input type="hidden" class="default_currency" name="default_currency" value="CAD"><input type="hidden" class="default_price_list" name="default_price_list" value=""><input type="hidden" class="address" name="address" value=""><input type="text" class="mso_notes" placeholder="MSO notes/Comments" name="mso_notes" value=""><div class="autocomplete"><input type="text"  placeholder="Customer"  id="isupplier' + colNum + '" class="isupplier" name="isupplier' + colNum + '" value=""></div><input type="text" placeholder="PO number"  class="po_no" name="po_no" value=""><div class="autocomplete"><input type="text" id="address_title' + colNum + '" placeholder="Customer Address"  class="address_title" name="address_title' + colNum + '" value=""></div></td>');
        } else if (row == 2) {
            $('td[data-row=' + row + '][data-col=' + (parseInt(colNum) - 1) + ']').after('<td data-row="' + row + '" data-col="' + colNum + '">Qty and Price</td>');
        } else {
            if (row == (rowCount - 1)) {
                $('td[data-row=' + row + '][data-col=' + (parseInt(colNum) - 1) + ']').after('<td data-row="' + row + '" data-col="' + colNum + '"><p id="qtotal" class="qtotal' + colNum + '">0</p><p id="stotal" class="stotal' + colNum + '">0.0</p></td>');
            } else {
                $('td[data-row=' + row + '][data-col=' + (parseInt(colNum) - 1) + ']').after('<td data-row="' + row + '" data-col="' + colNum + '"><input type="hidden" class="iname' + colNum + '" id="iname" name="iname' + colNum + '" value=""><input  id="rqty"  class="rqty' + colNum + '" type="hidden"  name="rqty' + colNum + '" value="0"><input  id="iqty"  class="iqty' + colNum + '" type="text"  name="iqty' + colNum + '" value="0"><input class="iprice' + colNum + '" type="text"  id="iprice" name="iprice' + colNum + '" value="0.0"></td>');
            }
        }
    }
}

function salesTemplatetable_IncrimentColIdNumber(startPosition, increment) {

    //increment column id's
    var cells = $('td[data-col]');

    //foreach cell
    for (i = 0; i < cells.length; i++) {

        var colNum = parseInt(cells.eq(i).attr('data-col'));

        //for every column beyond the insertion point, increment the column number
        if (colNum >= startPosition) {
            var newId = colNum + parseInt(increment);
            cells.eq(i).attr('data-col', newId);
            cells.eq(i).find('.delCol').attr('onClick', 'salesTemplatetable_DelCol(' + newId + ')');
            cells.eq(i).find('.isupplier').attr('id', 'isupplier' + newId);
            cells.eq(i).find('.address_title').attr('id', 'address_title' + newId);
            cells.eq(i).find('#iqty').attr('class', 'iqty' + newId);
            cells.eq(i).find('#iprice').attr('class', 'iprice' + newId);
            cells.eq(i).find('#iname').attr('class', 'iname' + newId);
            cells.eq(i).find('#rqty').attr('class', 'rqty' + newId);
            cells.eq(i).find('.isupplier').attr('name', 'isupplier' + newId);
            cells.eq(i).find('.address_title').attr('name', 'address_title' + newId);
            cells.eq(i).find('#iqty').attr('name', 'iqty' + newId);
            cells.eq(i).find('#iprice').attr('name', 'iprice' + newId);
            cells.eq(i).find('#iname').attr('name', 'iqty' + newId);
            cells.eq(i).find('#rqty').attr('name', 'iprice' + newId);
            cells.eq(i).find('#stotal').attr('class', 'stotal' + newId);
            cells.eq(i).find('#qtotal').attr('class', 'qtotal' + newId);
        }
    }
}

function salesTemplatetable_DelRow(row) {
    if ($("#salesTemplatetable tr").length > 5) {
        $('tr[data-row=' + row + ']').remove();

        salesTemplatetable_IncrimentRowIdNumber(row, -1);


        $('.sitems').each(function() {
            $(this).updatedata1();
        });


    } else {
        //alert("Can not delete row");
    }
}

function salesTemplatetable_DelCol(col) {
    var salesTemplatetable = $('#salesTemplatetable');
    var colCount = salesTemplatetable.find('td[data-row=0]').length;

    if (colCount > 7) {
        $('td[data-col=' + parseInt(col) + ']').remove();


        salesTemplatetable_IncrimentColIdNumber(col, -1);

        $('.sitems').each(function() {
            $(this).updatedata1();
        });
    } else {}
}


jQuery.fn.updatedata1 = function() {

    var row = $(this).parents('.item-row');

    var salesTemplatetable = $('#salesTemplatetable');
    var colCount = salesTemplatetable.find('td[data-row=0]').length;
    var wgtitotal = 0;
    var pltitotal = 0;
    var qtytotal = 0;
    var ppktotal = 0;
    var itotal = 0;
    var avgitotal = 0;
    var stotal = 0;
    var qtytotal = 0;
    var qtotal = 0;
    var purchase_pallets = parseFloat(row.find('.purchase_pallets').val());
    var ppk_calculation = parseFloat(row.find('.ppk_calculation').val());
    var weight = parseFloat(row.find('.weight').val());

    if (isNaN(purchase_pallets)) {
        purchase_pallets = row.find('.purchase_pallets').val(0);
    }
    if (isNaN(ppk_calculation)) {
        ppk_calculation = row.find('.ppk_calculation').val(0);
    }
    if (isNaN(weight)) {
        weight = row.find('.weight').val(0);
    }
	
	var usd = parseFloat($("input[data-fieldname*='usd']").val());
	
    for (var i = 4; i < (colCount-2); i++) {
		var sidcell = $("#isupplier"+i).parents('td');
		var default_currency = sidcell.find('.default_currency').val();
        var iqty = parseFloat(row.find('.iqty' + i).val());
        var iprice = parseFloat(row.find('.iprice' + i).val());

        if (isNaN(iqty)) {
            row.find('.iqty' + i).val(0);
            break;
        }
        if (isNaN(iprice)) {
            row.find('.iprice' + i).val(0.0);
            break;
        }
		
		if(default_currency == "USD") 
		{
			iprice = parseFloat(iprice / usd).toFixed(2);
		} 

        itotal = itotal + (iqty * iprice);
        qtytotal = qtytotal + iqty;
        ppktotal = ppktotal + (iqty * ppk_calculation);


        var qty = $('.iqty' + i);
        var price = $('.iprice' + i);

        for (var k = 0; k < qty.length; k++) {
            qtotal = qtotal + parseFloat(qty[k].value);
            stotal = stotal + (qty[k].value * price[k].value);
        } //alert(stotal);
        $('.stotal' + i).html(stotal);
        $('.qtotal' + i).html(qtotal);
        stotal = 0;
        qtotal = 0;
//console.log(i);
    }
//console.log(colCount);
    avgitotal = avgitotal + parseFloat(itotal / qtytotal);
    if (isNaN(avgitotal)) {
        avgitotal = 0;
    }
	var pp = parseFloat(qtytotal / purchase_pallets);
	if(isNaN(pp) || pp == 'Infinity') { pp = 0; }
	
	var ww = parseFloat(qtytotal * weight);
	if(isNaN(ww)) { ww = 0; }
	
	row.find('.qtytotal').html(qtytotal);
	var qtytotal_total = 0;
    $(".qtytotal").each(function() {
		if(isNaN(parseFloat($(this).html()))) 
		{ } 
		else {
			qtytotal_total += parseFloat($(this).html());
		}
    });
	
	row.find('.ppktotal').html(ppktotal);
	var ppktotal_total = 0;
    $(".ppktotal").each(function() {
		if(isNaN(parseFloat($(this).html()))) 
		{ } 
		else {
			ppktotal_total += parseFloat($(this).html());
		}
    });
	$('.ppktotal_total').html(ppktotal_total);
	document.querySelector('div[data-fieldname="numbers_boxes"] .control-input-wrapper .control-value').innerHTML = qtytotal_total;
}


function autocomplete2(idd) {
    inp = document.getElementById(idd);

    /*An array containing all the country names in the world:*/

    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;


        $.ajax({
            url: '/api/resource/Item/?fields=["name", "item_code", "item_name", "description", "weight_per_unit","weight_of_pallets","sale_pallets","gross_weight","stock_uom","ppk_calculation"]&limit_page_length=0',
            type: 'get',
            dataType: "json",
            success: function(r) {
                for (i = 0; i < r.data.length; i++) {
                    //console.log(r.data.length);
                    /*check if the item starts with the same letters as the text field value:*/
                    if (r.data[i]['item_code'].toUpperCase().includes(val.toUpperCase())) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = r.data[i]['item_code'];
                        /*insert a input field that will hold the current array item's value:*/
						var gw = r.data[i]['gross_weight'];
						if(isNaN(r.data[i]['gross_weight'])) { gw = 0; }
						var ppkc = r.data[i]['ppk_calculation'];
						if(isNaN(r.data[i]['ppk_calculation'])) { ppkc = 0; }
						
						 b.innerHTML += '<input type="hidden" class="itmname" value="' + r.data[i]['item_name'] + '"><input type="hidden" class="itmid" value="' + r.data[i]['name'] + '"><input type="hidden" class="itmcode" value="' + r.data[i]['item_code'] + '"><input type="hidden" class="itmppk" value="' + ppkc + '"><input type="hidden" class="itmweight" value="' + r.data[i]['weight_per_unit'] + '"><input type="hidden" class="itmpgweight" value="' + gw + '"><input type="hidden" class="itmuom" value="' + r.data[i]['stock_uom'] + '"><input type="hidden" class="itmplt" value="' + r.data[i]['sale_pallets'] + '"><span  class="idesc" style="display:none">' + r.data[i]['description'] + '</span>';
						
                       // b.innerHTML += "<input type='hidden' class='itmname' value='" + r.data[i]['item_name'] + "'><input type='hidden' class='itmid' value='" + r.data[i]['name'] + "'><input type='hidden' class='itmcode' value='" + r.data[i]['item_code'] + "'><input type='hidden' class='itmweight' value='" + r.data[i]['weight_per_unit'] + "'><input type='hidden' class='itmpgweight' value='" + gw + "'><input type='hidden' class='itmuom' value='" + r.data[i]['stock_uom'] + "'><input type='hidden' class='itmplt' value='" + r.data[i]['sale_pallets'] + "'><span  class='idesc' style='display:none'>" + r.data[i]['description'] + "</span>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function(e) {
                            /*insert the value for the autocomplete text field:*/
                            inp.value = this.getElementsByClassName("itmcode")[0].value;
                            var row = $("#" + idd).parents('.item-row');
                            row.find('.sitemsid').val(this.getElementsByClassName("itmid")[0].value);
                            row.find('.item_code').val(this.getElementsByClassName("itmcode")[0].value);
                            row.find('.weight').val(this.getElementsByClassName("itmweight")[0].value);
                            row.find('.gross_weight').val(this.getElementsByClassName("itmpgweight")[0].value);
                            row.find('.uom').val(this.getElementsByClassName("itmuom")[0].value);
                            row.find('.purchase_pallets').val(this.getElementsByClassName("itmplt")[0].value);
                            row.find('.idesc').val(this.getElementsByClassName("itmname")[0].value);
							row.find('.ppk_calculation').val(this.getElementsByClassName("itmppk")[0].value);


                            var salesTemplatetable = $('#salesTemplatetable');
                            var colCount = salesTemplatetable.find('td[data-row=0]').length;

                            var wgtitotal = 0;
							var pltitotal = 0;
							var qtytotal = 0;
							var ppktotal = 0;
							var itotal = 0;
							var avgitotal = 0;
							var stotal = 0;
							var qtytotal = 0;
							var qtotal = 0;
							var purchase_pallets = parseFloat(row.find('.purchase_pallets').val());
							var ppk_calculation = parseFloat(row.find('.ppk_calculation').val());
							var weight = parseFloat(row.find('.weight').val());

							if (isNaN(purchase_pallets)) {
								purchase_pallets = row.find('.purchase_pallets').val(0);
							}
							if (isNaN(ppk_calculation)) {
								ppk_calculation = row.find('.ppk_calculation').val(0);
							}
                            if (isNaN(weight)) {
                                weight = row.find('.weight').val(0);
                            }
							var usd = parseFloat($("input[data-fieldname*='usd']").val());
							
							 for (var i = 4; i < (colCount-2); i++) 
							 {
								var sidcell = $("#isupplier"+i).parents('td');
								var default_currency = sidcell.find('.default_currency').val();
								var price_list = sidcell.find('.default_price_list').val();
								var rowid ="#"+idd;
								var column = '.iprice' + i;
								var suppliername = $("#isupplier"+i).val();
								
									frappe.call({
										method:'erpnext.api2.customerPriceList',
										args: {
											row: rowid,
											column: column,
											supplier: suppliername,
											item: inp.value,
											price_list: price_list,
										 },
										callback: function(r) {
											console.log(r.message);
											var row1 = $(r.message[0].row).parents('.item-row');
											row1.find(r.message[0].column).val(r.message[0].price);
											
										}
								   });
								
								var iqty = parseFloat(row.find('.iqty' + i).val());
								var iprice = parseFloat(row.find('.iprice' + i).val());

								if (isNaN(iqty)) {
									row.find('.iqty' + i).val(0);
									break;
								}
								if (isNaN(iprice)) {
									row.find('.iprice' + i).val(0.0);
									break;
								}
								
								if(default_currency == "USD") 
								{
									iprice = parseFloat(iprice / usd).toFixed(2);
								} 

                                itotal = itotal + (iqty * iprice);
                                qtytotal = qtytotal + iqty;
								ppktotal = ppktotal + (iqty * ppk_calculation);

                                var qty = $('.iqty' + i);
                                var price = $('.iprice' + i);

                                for (var k = 0; k < qty.length; k++) {
                                    qtotal = qtotal + parseFloat(qty[k].value);
                                    stotal = stotal + (qty[k].value * price[k].value);
                                } //alert(stotal);
                                $('.stotal' + i).html(stotal);
                                $('.qtotal' + i).html(qtotal);
                                stotal = 0;
                                qtotal = 0;
                            }
                            avgitotal = avgitotal + parseFloat(itotal / qtytotal);
                            if (isNaN(avgitotal)) {
                                avgitotal = 0;
                            }
							var pp = parseFloat(qtytotal / purchase_pallets);
								if (isNaN(pp) || pp == 'Infinity') { pp = 0; }
								
								var ww = parseFloat(qtytotal * weight);
								if (isNaN(ww)) { ww = 0; }
							
							row.find('.qtytotal').html(qtytotal);
							var qtytotal_total = 0;
							$(".qtytotal").each(function() {
								if(isNaN(parseFloat($(this).html()))) 
								{ } 
								else {
									qtytotal_total += parseFloat($(this).html());
								}
							});
							
							row.find('.ppktotal').html(ppktotal);
							var ppktotal_total = 0;
							$(".ppktotal").each(function() {
								if(isNaN(parseFloat($(this).html()))) 
								{ } 
								else {
									ppktotal_total += parseFloat($(this).html());
								}
							});
							$(".ppktotal_total").html(ppktotal_total);
							document.querySelector('div[data-fieldname="numbers_boxes"] .control-input-wrapper .control-value').innerHTML = qtytotal_total;
                          /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                        });
                        a.appendChild(b);
                    }
                    //if(inp.value == arr[i]) { chk = true;}
                }
            }
        });
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        var chk = false;

    });
    // if(chk == false ) { inp.value = ""; }
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}


function autocompletesupplier2(idd) {
    sinp = document.getElementById(idd);

    /*An array containing all the country names in the world:*/



    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    sinp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        $.ajax({
            url: '/api/resource/Customer/?fields=["name", "customer_name", "default_currency","default_price_list"]&limit_page_length=0',
            type: 'get',
            dataType: "json",
            success: function(r) {
                for (i = 0; i < r.data.length; i++) {
                    //console.log(r.message.length);
                    /*check if the item starts with the same letters as the text field value:*/
                    if (r.data[i]['customer_name'].toUpperCase().includes(val.toUpperCase())) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = r.data[i]['customer_name'];
                        /*insert a input field that will hold the current array item's value:*/
						var dpl = "STD";
						if(r.data[i]['default_price_list'] != "undefined" && r.data[i]['default_price_list'] && r.data[i]['default_price_list'] != null) { dpl = r.data[i]['default_price_list'];}
						
						 b.innerHTML += '<input type="hidden" class="sitmname" value="' + r.data[i]['name'] + '"><input type="hidden" class="sitmid" value="' + r.data[i]['name'] + '"><input type="hidden" class="sitmpl" value="' + dpl + '"><input type="hidden" class="sitmcurrency" value="' + r.data[i]['default_currency'] + '"><span style="display:none"   class="sidesc">' + r.data[i]['name'] + '</span>';
						
                        //b.innerHTML += "<input type='hidden' class='itmname' value='" + r.data[i]['name'] + "'><input type='hidden' class='itmid' value='" + r.data[i]['name'] + "'><input type='hidden' class='itmpl' value='" + r.data[i]['default_price_list'] + "'><input type='hidden' class='itmcurrency' value='" + r.data[i]['default_currency'] + "'><span style='display:none'   class='idesc'>" + r.data[i]['customer_name'] + "</span>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function(e) {
                            /*insert the value for the autocomplete text field:*/
                            sinp.value = this.getElementsByClassName("sitmname")[0].value; //alert(sinp.value );

                             var sidcell = $("#" + idd).parents('td');
							if(!this.getElementsByClassName("sitmpl")[0].value || this.getElementsByClassName("sitmpl")[0].value == null) { var df_pl = ""; } else {  var df_pl = this.getElementsByClassName("sitmpl")[0].value;  }
                            sidcell.find('.isupplierid').val(this.getElementsByClassName("sitmid")[0].value);
                            sidcell.find('.default_price_list').val(df_pl);
                            sidcell.find('.default_currency').val(this.getElementsByClassName("sitmcurrency")[0].value);
							
							var column1 = '#'+ idd.replace("isupplier", "address_title");
							var suppliername1 = sinp.value;
							
							frappe.call({
										method:'erpnext.api2.customerAddress',
										args: {
											column: column1,
											supplier: suppliername1,
										 },
										callback: function(r) {
											console.log(r.message);
											$(r.message[0].column).val(r.message[0].address_title);
											var sidcells = $(r.message[0].column).parents('td');
											sidcells.find('.address').val(r.message[0].address);
											
										}
							 });
							
							$('.sitems').each(function() {
								var row = $(this).parents('.item-row');
								var price_list = df_pl;
								var rowid ="#"+$(this).attr('id');
								var column = '.'+ idd.replace("isupplier", "iprice");
								var suppliername = sinp.value;
								var price = row.find(column).val();
								if(row.find('.item_code').val() != '')
								{
									frappe.call({
										method:'erpnext.api2.customerPriceList',
										args: {
											row: rowid,
											column: column,
											supplier: suppliername,
											item: $(this).val(),
											price_list: price_list,
										 },
										callback: function(r) {
											console.log(r.message);
											var row1 = $(r.message[0].row).parents('.item-row');
											row1.find(r.message[0].column).val(r.message[0].price);
											
										}
								   });
								}
								
							});


                            /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                        });
                        a.appendChild(b);
                    }

                }
            }
        });
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        var chk = false;

    });
    // if(chk == false ) { sinp.value = ""; }
    /*execute a function presses a key on the keyboard:*/
    sinp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != sinp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}

function autocompleteaddress2(idd) {
    ainp = document.getElementById(idd);
	var column1 = '#'+ idd.replace("address_title", "isupplier");
	var suppliernamee = $(column1).val();

    /*An array containing all the country names in the world:*/



    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    ainp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        frappe.call({
			method:'erpnext.salesapi.customerAddresses',
			args: {
					supplier: suppliernamee
				},
			callback: function(r) {
				//console.log(r); return false;
                for (i = 0; i < r.message.length; i++) {
                    //console.log(r.message.length);
                    /*check if the item starts with the same letters as the text field value:*/
                    if (r.message[i]['name'].toUpperCase().includes(val.toUpperCase())) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = r.message[i]['name'];
                        /*insert a input field that will hold the current array item's value:*/
						 b.innerHTML += '<input type="hidden" class="sitmname" value="' + r.message[i]['name'] + '"><input type="hidden" class="saddress_title" value="' + r.message[i]['address_title'] + '">';
						
                        b.addEventListener("click", function(e) {
                            /*insert the value for the autocomplete text field:*/
                            ainp.value = this.getElementsByClassName("saddress_title")[0].value; //alert(ainp.value );
							var sidcellss = $("#"+idd).parents('td');
							sidcellss.find('.address').val(this.getElementsByClassName("sitmname")[0].value);
							
                            /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                        });
                        a.appendChild(b);
                    }

                }
            }
        });
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        var chk = false;

    });
    // if(chk == false ) { ainp.value = ""; }
    /*execute a function presses a key on the keyboard:*/
    ainp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != ainp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}
