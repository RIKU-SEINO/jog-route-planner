document.addEventListener('DOMContentLoaded', function () {
  const maxImages = 6;

  function readURL(input, previewId, textId) {
      if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
              var preview = document.getElementById(previewId);
              var text = document.getElementById(textId);
              preview.style.display = 'block';
              preview.src = e.target.result;
              if (text) {
                  text.style.display = 'none';
              }
              // 新しい空のフィールドを追加
              let allFields = document.querySelectorAll('div.upload-field')
              addUploadField(allFields.length + 1);
              let allDivsWithSpans = document.querySelectorAll('div.upload-field:has(span)'); // 子孫に span を持つ全ての div
              let filteredDivs = [...allDivsWithSpans].filter(div => {
                let spans = div.querySelectorAll('span');
                return !Array.from(spans).some(span => span.style.display === 'none');
              });
              for (i=filteredDivs.length-1; i>0; i--) {
                filteredDivs[i].remove();
              }
              if (document.querySelectorAll('div.upload-field').length > maxImages) {filteredDivs[0].remove();}
          }
          reader.readAsDataURL(input.files[0]);
      }
  }

  function addUploadField(index) {
      var uploadFieldsDiv = document.querySelector('.upload-fields');
      var newUploadField = document.createElement('div');
      newUploadField.classList.add('upload-field');
      newUploadField.setAttribute('id', 'upload-field-' + index);

      var label = document.createElement('label');
      label.setAttribute('for', 'file-input-' + index);
      label.classList.add('upload-label');

      var input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.classList.add('file-input');
      input.setAttribute('id', 'file-input-' + index);
      input.setAttribute('name', 'course_images');
      
      var span = document.createElement('span');
      span.classList.add('upload-text');
      span.setAttribute('id', 'upload-text-' + index);
      span.textContent = 'クリックしてコースの写真をアップロード';

      var img = document.createElement('img');
      img.setAttribute('id', 'preview-' + index);
      img.classList.add('image-preview');
      img.style.display = 'none';

      label.appendChild(input);
      label.appendChild(span);
      label.appendChild(img);
      newUploadField.appendChild(label);
      uploadFieldsDiv.appendChild(newUploadField);

      input.addEventListener('change', function () {
          readURL(input, 'preview-' + index, 'upload-text-' + index);
      });
  }

  // 初期アップロードフィールドの追加
  if (document.querySelectorAll('.upload-field').length === 0) {
      addUploadField(1);
  }

  // 既存のファイル入力要素にイベントリスナーを追加
  var fileInputs = document.querySelectorAll('.file-input');
  fileInputs.forEach(function (input) {
      input.addEventListener('change', function () {
          var index = input.id.split('-').pop();
          var previewId = 'preview-' + index;
          var textId = 'upload-text-' + index;
          readURL(input, previewId, textId);
      });
  });
});

function saveUpdatedIndex(index) {
    // 隠しフィールドにインデックスの値を設定する
    let courseImages = parseCourseImageString(document.getElementById("course-info-image").getAttribute("data-course"));
    if (index <= courseImages.length) {
        //以前にアップロードした画像フィールドに新たに画像を上書きアップロードしたので、backend側でupdate
        let arrayStr = document.getElementById('updated_image_indices').getAttribute("value");
        let array = JSON.parse(arrayStr);
        array.push(index-1);
        document.getElementById('updated_image_indices').value = JSON.stringify(array);
    }
}

function parseCourseImageString(str) {
    // 文字列から不要な部分を取り除く
    let cleanedStr = str.replace(/[\[\]<>]/g, ''); // 角括弧と山括弧を削除
    let parts = cleanedStr.split(', '); // 各項目を分割

    // 各項目を解析し、JSONオブジェクトの配列を作成
    let jsonArray = parts.map(part => {
        let [className, id] = part.split(' '); // クラス名とIDを分割
        return {
            className: className,
            id: parseInt(id) // 数値として扱うためにパース
        };
    });

    // JSON文字列に変換
    return jsonArray;
}
