$(document).ready(function () {

            $("#submit").click(function (event) {
                let filled = true;
                $('input:text').each(function () {
                    if ($(this).val().length === 0){
                        filled = false;
                        return false;
                    }

                })
                if (filled === true){
                    alert('Successful...');
                }
            })
        });