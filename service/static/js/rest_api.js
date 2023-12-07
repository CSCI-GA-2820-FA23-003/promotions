$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        console.log(res.start)
        $("#promotion_id").val(res.id);
        $("#promotion_code").val(res.code);
        $("#promotion_name").val(res.name);
        $("#promotion_start").val((res.start).slice(0,10));
        $("#promotion_expired").val((res.expired).slice(0,10));
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
        $("#promotion_category").val("");
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
        let category = $("#promotion_category").val();
        let available = $("#promotion_available").val();
        let whole_store = $("#promotion_whole_store").val() == "true";
        let promo_type = $("#promotion_promo_type").val();

        let data = {
            "code": code,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "category": category,
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

        let code = $("#promotion_code").val();
        let category = $("#promotion_category").val();
        let available = $("#promotion_available").val();

        let queryString = ""

        if (code) {
            queryString += 'code=' + code
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/promotions?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

