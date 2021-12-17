$(document).ready(function () {
  var counter = 0;
  var categoryList = {};

  $('body').ready(function(){
    $('#newCategory').trigger('click');
  });

  $('#newCategory').click(function(){
    var categoryForm = `<div class="form-group col-lg-3 col-sm-5 col-12 shadow py-3 mx-lg-4 mx-sm-4 mx-auto my-3 rounded bg-primary" id="category${++counter}">
                          <div class="px-3 row">
                            <label class="col-form-label text-white my-auto">Category ${counter} Name</label>
                            <svg width="16" height="16" fill="#ffffff" class="bi bi-dash-circle-fill align-middle ml-auto remove-form" viewBox="0 0 16 16" id="category${counter}">
                              <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1h-7z"/>
                            </svg>
                          </div>
                          <input class="form-control mt-4 categoryInput" type="text" id="title${counter}" name="title${counter}" placeholder="Enter category title ..." autocomplete="off">
                        </div>`;
    $("#categoryList").append(categoryForm);
    categoryList['category'+counter] = 'title'+counter;
    $("#submitBtn").prop("disabled", true);
  });

  $(document).on('click', '.remove-form', function(){
    var id = this.id;
    $('#'+id).remove();
    delete categoryList[id];
    $('.categoryInput').trigger('keyup');
  });

  $(document).on('keyup', '.categoryInput', () => {
    var counter = 0;
    var len = 0;

    $.each(categoryList, (key, val) => {
      len++;
      if ($("#"+val).val())
        counter++;
    });
    
    $("#submitBtn").prop("disabled", () => {
      if (len == counter) return false;
      else return true;
    });
  });
});
