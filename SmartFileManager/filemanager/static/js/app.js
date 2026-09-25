document.addEventListener("DOMContentLoaded", function () {

    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const selectedFiles = document.getElementById("selectedFiles");
    const uploadForm = document.getElementById("uploadForm");

    if (!dropZone || !fileInput) {
        return;
    }


    // =====================================================
    // STORE SELECTED FILES
    // =====================================================

    let selectedFileList = [];


    // =====================================================
    // SHOW SELECTED FILES
    // =====================================================

    function displayFiles() {

        selectedFiles.innerHTML = "";

        if (selectedFileList.length === 0) {
            return;
        }


        selectedFileList.forEach(function (file, index) {

            const fileRow = document.createElement("div");

            fileRow.className = "selected-file-row";


            fileRow.innerHTML = `

                <div class="selected-file-info">

                    <i class="bi bi-file-earmark"></i>

                    <div>

                        <strong>
                            ${file.name}
                        </strong>

                        <small>
                            ${formatFileSize(file.size)}
                        </small>

                    </div>

                </div>


                <button
                    type="button"
                    class="remove-file"
                    data-index="${index}"
                >
                    <i class="bi bi-x"></i>
                </button>

            `;


            selectedFiles.appendChild(fileRow);

        });


        // Remove buttons

        document
            .querySelectorAll(".remove-file")
            .forEach(function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const index =
                            parseInt(
                                this.dataset.index
                            );

                        selectedFileList.splice(
                            index,
                            1
                        );

                        updateFileInput();

                        displayFiles();

                    }
                );

            });

    }


    // =====================================================
    // FORMAT FILE SIZE
    // =====================================================

    function formatFileSize(bytes) {

        if (bytes === 0) {
            return "0 Bytes";
        }

        const units = [
            "Bytes",
            "KB",
            "MB",
            "GB"
        ];

        const index = Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        );

        return (
            parseFloat(
                (
                    bytes /
                    Math.pow(
                        1024,
                        index
                    )
                ).toFixed(2)
            )
            +
            " "
            +
            units[index]
        );

    }


    // =====================================================
    // UPDATE FILE INPUT
    // =====================================================

    function updateFileInput() {

        const dataTransfer =
            new DataTransfer();

        selectedFileList.forEach(
            function (file) {

                dataTransfer.items.add(
                    file
                );

            }
        );

        fileInput.files =
            dataTransfer.files;

    }


    // =====================================================
    // FILE INPUT
    // =====================================================

    fileInput.addEventListener(
        "change",
        function () {

            selectedFileList =
                Array.from(
                    fileInput.files
                );

            displayFiles();

        }
    );


    // =====================================================
    // DRAG OVER
    // =====================================================

    dropZone.addEventListener(
        "dragover",
        function (event) {

            event.preventDefault();

            dropZone.classList.add(
                "drag-over"
            );

        }
    );


    // =====================================================
    // DRAG LEAVE
    // =====================================================

    dropZone.addEventListener(
        "dragleave",
        function () {

            dropZone.classList.remove(
                "drag-over"
            );

        }
    );


    // =====================================================
    // DROP
    // =====================================================

    dropZone.addEventListener(
        "drop",
        function (event) {

            event.preventDefault();

            dropZone.classList.remove(
                "drag-over"
            );


            const droppedFiles =
                Array.from(
                    event.dataTransfer.files
                );


            selectedFileList =
                selectedFileList.concat(
                    droppedFiles
                );


            updateFileInput();

            displayFiles();

        }
    );


    // =====================================================
    // PREVENT DROP OUTSIDE DROP ZONE
    // =====================================================

    document.addEventListener(
        "dragover",
        function (event) {

            event.preventDefault();

        }
    );


    document.addEventListener(
        "drop",
        function (event) {

            if (
                !dropZone.contains(
                    event.target
                )
            ) {

                event.preventDefault();

            }

        }
    );


    // =====================================================
    // FORM SUBMIT
    // =====================================================

    if (uploadForm) {

        uploadForm.addEventListener(
            "submit",
            function (event) {

                if (
                    selectedFileList.length === 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please select at least one file."
                    );

                }

            }
        );

    }

});