window.onload = (event) => {
    console.log('init....')
}
const root = ReactDOM.createRoot(document.getElementById("root"));
const App = () => {

    const { useState } = React;
    const [selectedFile, setSelectedFile] = useState();
    const [checkFile, setCheckFile] = useState(false);

    const imageHandler = (e) => {
        setSelectedFile(e.target.files[0]);
        setCheckFile(true);
    }

    const imagesubmission = () => {
        if (checkFile) {
            alert("Archivo Cargdo");
            console.log(selectedFile);
        } else {
            alert("Selecciona Archivo");
        }
    }

    return (
        <>
            <div className="h-screen bg-gray-300 flex justify-center items-center px-2">
                <div className="w-[320px] grid gap-2">
                    <div className="h-24 cursor-pointer relative flex justify-center items-center border-2 rounded-md bg-gray-200">
                        <input type="file" name="file" onChange={imageHandler} className="z-20 opacity-0 cursor-pointer h-full w-full" />
                        <div className="absolute flex justify-center items-center gap-2">
                            <img className={`h-10 w-10 rounded-full ${checkFile?'opacity-1':'opacity-0'}`} src={selectedFile ? URL.createObjectURL(selectedFile) : null} />
                            <span className="text-[18px] w-56 truncate">{checkFile?selectedFile.name:'choose a file'}</span>
                        </div>        
                    </div>
                    <button onClick={imagesubmission} className="w-full h-14 bg-green-600 text-white rounded-md">Upload</button>
                </div>
            </div>
        </>
    );
}

root.render(<App />);