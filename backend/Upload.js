import React, { useState, useDropzone } from "react";

const Upload = () => {
  const [files, setFiles] = useState([]);

  const onDrop = (event) => {
    const files = event.dataTransfer.files;
    setFiles(files);
  };

  return (
    <div>
      <input type="file" onChange={onDrop} />
      <ul>
        {files.map((file) => (
          <li key={file.name}>{file.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Upload;