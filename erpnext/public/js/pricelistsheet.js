
function myTable_IncrimentRowIdNumber(startPosition, increment) {
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
            items.eq(i).find('.del').attr('onClick', 'myTable_DelRow(' + newId + ')');
            items.eq(i).find('.price_list_data').attr('id', 'price_list_data' + newId);
            items.eq(i).find('.price_list_data').attr('onclick', "autocomplete1('price_list_data"+ newId + "')");
        }
    }
}

function AddNewRow1() {
    //using jquery, grab a reference to the html table
    var myTable = $('#qtyTable1');
    //get the number of rows and columns
    var colCount = myTable.find('td[data-row=0]').length;
    var rowCount = $("#qtyTable1 tr").length;
    row = rowCount; //rowCount - 1
    //incriment position numbers to make room for the new row
    //this is required to keep things working after we change the table
    myTable_IncrimentRowIdNumber(row, 1);

    //add row
    var newRow = '<tr data-row="' + row + '" class="item-row">';
    //add cells into the row
	newRow=newRow+'<td width="20px" data-row="'+row+'" data-col="0"><a href="javascript:;" class="del" onClick="myTable_DelRow('+row+')">X</a></td><td data-row="'+row+'" data-col="1"><div class="autocomplete"><input onClick="autocomplete1(\'price_list_data'+row+'\')" type="text" class="price_list_data" id="price_list_data'+row+'" name="price_list_data" value=""></div></td>';
    //close the row
    newRow += '</tr>';
    $(newRow).insertAfter('tr[data-row=' + (parseInt(row) - 1) + ']');
}


function myTable_DelRow(row) {
    if ($("#qtyTable1 tr").length > 2) {
        $('tr[data-row=' + row + ']').remove();

        myTable_IncrimentRowIdNumber(row, -1);


        $('.price_list_data').each(function() {
            //$(this).updatedata();
        });


    } else {
        //alert("Can not delete row");
    }
}


function autocomplete1(idd) {
    inp = document.getElementById(idd);
	
    /*An array containing all the country names in the world:*/

    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;


        $.ajax({
            url: '/api/resource/Price List/?fields=["name"]&limit_page_length=0',
            type: 'get',
            dataType: "json",
            success: function(r) {
                for (i = 0; i < r.data.length; i++) {
                    //console.log(r.data.length);
                    /*check if the item starts with the same letters as the text field value:*/
                    if (r.data[i]['name'].toUpperCase().includes(val.toUpperCase())) {
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = r.data[i]['name'];
                        /*insert a input field that will hold the current array item's value:*/
                        b.innerHTML += "<input type='hidden' class='pricelstname' value='" + r.data[i]['name'] + "'>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function(e) {
                            /*insert the value for the autocomplete text field:*/
                            inp.value = this.getElementsByClassName("pricelstname")[0].value;
							
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
