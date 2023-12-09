$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the  ponse
    function update_form_data(res) {
        console.log(res.start)
        $("#promotion_id").val(res.id);
        $("#promotion_code").val(res.code);
        $("#promotion_name").val(res.name);
        $("#promotion_start").val((res.start).slice(0,10));
        $("#promotion_expired").val((res.start).slice(0,10));
        $("#promotion_available").val(res.available);
        $("#promotion_wholestore").val(res.whole_store.toString());
        $("#promotion_type").val(res.promo_type);
    }
    // Clears all form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_code").val("");
        $("#promotion_name").val("");
        $("#promotion_start").val("");
        $("#promotion_expired").val("");
        $("#promotion_available").val("");
        $("#promotion_wholestore").val("");
        $("#promotion_type").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        let code = $("#promotion_code").val();
        let name = $("#promotion_name").val();
        let start = $("#promotion_start").val(); // Adjusted to match model attribute
        let expired = $("#promotion_expired").val(); // Adjusted to match model attribute
        let available = parseInt($("#promotion_available").val()); // Ensuring it is an integer
        let whole_store = $("#promotion_wholestore").val()=== 'true'; // Ensuring it is a boolean
        let value = parseFloat($("#promotion_type").val()); 
        let promo_type = parseInt($("#promotion_type").val());// Assuming there's an input for value

        let data = {
            "code": code,
            "name": name,
            "start": start,
            "expired": expired,
            "available": available,
            "whole_store": whole_store,
            "promo_type": promo_type,
            "value": value // Assuming you want to include this, it should be a part of your form
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/promotions", // Make sure this endpoint matches your Flask route
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            // Assuming your response includes the full promotion object
            update_form_data(res); // You'll need to create this function to handle the response
            flash_message("Promotion created successfully"); // Adjust the message as needed
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message); // Error handling message
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let promotion_id = $("#promotion_id").val();
        let code = $("#promotion_code").val();
        let name = $("#promotion_name").val();
        let start_date = $("#promotion_start_date").val();
        let end_date = $("#promotion_end_date").val();
        let available = $("#promotion_available").val();
        let whole_store = $("#promotion_whole_store").val() == "true";
        let promo_type = $("#promotion_promo_type").val();

        let data = {
            "code": code,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "available": available,
            "whole_store": whole_store,
            "promo_type": promo_type
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/promotions/${promotion_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            console.log("This will be output to the console");
            console.log("Value of start date:", res.start);
            console.log("Value of expired date:", res.expired);

            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/promotions/${promotion_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            console.log("This will be output to the console");
            console.log("Value of start date:", res.start);
            console.log("Value of expired date:", res.expired);
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let promotion_id = $("#promotion_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/promotions/${promotion_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data()
        $("#flash_message").empty();
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {
        let code = $("#promo_code").val();
        let name = $("#promo_name").val();
        let available = $("#promo_available").val();

        let queryString = "";

        if (code) {
            if (queryString.length > 0) {
                queryString += '&code=' + code;
            } else {
                queryString += 'code=' + code;
            }
        }

        if (name) {
            if (queryString.length > 0) {
                queryString += '&name=' + name;
            } else {
                queryString += 'name=' + name;
            }
        }

        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available;
            } else {
                queryString += 'available=' + available;
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th class="col-md-2">ID</th>';
            table += '<th class="col-md-2">Code</th>';
            table += '<th class="col-md-2">Name</th>';
            table += '<th class="col-md-2">Start Date</th>';
            table += '<th class="col-md-2">End Date</th>';
            table += '<th class="col-md-2">Available</th>';
            table += '<th class="col-md-2">Whole Store</th>';
            table += '<th class="col-md-2">Promo Type</th>';
            table += '</tr></thead><tbody>';
            
            let firstPromo = "";

            for(let i = 0; i < res.length; i++) {
                let promo = res[i];
                let start = promo.start.slice(0, 10);
                let expired = promo.expired.slice(0, 10);
                table +=  `<tr id="row_${i}">
                                <td>${promo.id}</td>
                                <td>${promo.code}</td>
                                <td>${promo.name}</td>
                                <td>${start}</td>
                                <td>${expired}</td>
                                <td>${promo.available}</td>
                                <td>${promo.whole_store}</td>
                                <td>${promo.promo_type}</td>
                            </tr>`;
                
                if (i === 0) {
                    firstPromo = promo;
                }
            }

            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPromo !== "") {
                update_form_data(firstPromo);
            }

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

    })

