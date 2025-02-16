const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

// tinymce.init({
//     selector: 'textarea#file-picker',
//     plugins: 'image code',
//     toolbar: 'undo redo | link image | code',
//     /* enable title field in the Image dialog*/
//     image_title: true,
//     /* enable automatic uploads of images represented by blob or data URIs*/
//     automatic_uploads: true,
//     /*
//       URL of our upload handler (for more details check: https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_url)
//       images_upload_url: 'postAcceptor.php',
//       here we add custom filepicker only to Image dialog
//     */
//     file_picker_types: 'image',
//     /* and here's our custom image picker*/
//     file_picker_callback: (cb, value, meta) => {
//         const input = document.createElement('input');
//         input.setAttribute('type', 'file');
//         input.setAttribute('accept', 'image/*');

//         input.addEventListener('change', (e) => {
//             const file = e.target.files[0];

//             const reader = new FileReader();
//             reader.addEventListener('load', () => {
//                 /*
//                   Note: Now we need to register the blob in TinyMCEs image blob
//                   registry. In the next release this part hopefully won't be
//                   necessary, as we are looking to handle it internally.
//                 */
//                 const id = 'blobid' + (new Date()).getTime();
//                 const blobCache = tinymce.activeEditor.editorUpload.blobCache;
//                 const base64 = reader.result.split(',')[1];
//                 const blobInfo = blobCache.create(id, file, base64);
//                 blobCache.add(blobInfo);

//                 /* call the callback and populate the Title field with the file name */
//                 cb(blobInfo.blobUri(), { title: file.name });
//             });
//             reader.readAsDataURL(file);
//         });

//         input.click();
//     },
//     content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
// });

language = ''
langCode = document.documentElement.getAttribute('data-lang')
if (langCode == 'ar') {
    language = 'ar'

}
else {
    language = 'fr_FR'
}

tinymce.init({
    selector: '.tiny-text-area',
    language : language,
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons accordion',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: "undo redo | accordion accordionremove | blocks fontfamily fontsize | bold italic underline strikethrough | align numlist bullist | link image | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor codesample | ltr rtl",
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [
        { title: 'My page 1', value: 'https://www.tiny.cloud' },
        { title: 'My page 2', value: 'http://www.moxiecode.com' }
    ],
    image_list: [
        { title: 'My page 1', value: 'https://www.tiny.cloud' },
        { title: 'My page 2', value: 'http://www.moxiecode.com' }
    ],
    image_class_list: [
        { title: 'None', value: '' },
        { title: 'Some class', value: 'class-name' }
    ],
    importcss_append: true,
    /* enable title field in the Image dialog*/
    image_title: true,
    /* enable automatic uploads of images represented by blob or data URIs*/
    automatic_uploads: true,
    /*
      URL of our upload handler (for more details check: https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_url)
      images_upload_url: 'postAcceptor.php',
      here we add custom filepicker only to Image dialog
    */
    file_picker_types: 'image',
    /* and here's our custom image picker*/
    file_picker_callback: (cb, value, meta) => {
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.addEventListener('change', (e) => {
            const file = e.target.files[0];

            const reader = new FileReader();
            reader.addEventListener('load', () => {
                /*
                  Note: Now we need to register the blob in TinyMCEs image blob
                  registry. In the next release this part hopefully won't be
                  necessary, as we are looking to handle it internally.
                */
                const id = 'blobid' + (new Date()).getTime();
                const blobCache = tinymce.activeEditor.editorUpload.blobCache;
                const base64 = reader.result.split(',')[1];
                const blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);

                /* call the callback and populate the Title field with the file name */
                cb(blobInfo.blobUri(), { title: file.name });
            });
            reader.readAsDataURL(file);
        });

        input.click();
    },
    height: 360,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
    setup: function (editor) {
        editor.on('change', function () {
            tinymce.triggerSave(); // Save content back to the textarea when changed
        });
    }
});