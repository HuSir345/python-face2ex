let pic1Data = null;
let pic2Data = null;

function setupFileUpload(buttonId, inputId, callback) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);
    
    button.addEventListener('click', () => {
        input.click();
    });
    
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            processFile(file, button, callback);
        }
    });
    
    button.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        button.classList.add('border-blue-500');
    });
    
    button.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        button.classList.remove('border-blue-500');
    });
    
    button.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        button.classList.remove('border-blue-500');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            processFile(file, button, callback);
        }
    });
}

function processFile(file, button, callback) {
    if (!file.type.startsWith('image/')) {
        alert('请选择图片文件');
        return;
    }
    
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('图片大小不能超过10MB');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
        try {
            const base64Data = e.target.result.split(',')[1];
            
            button.innerHTML = `
                <div class="relative w-full h-full">
                    <img src="${e.target.result}" class="w-full h-full object-cover rounded-xl" alt="已选择图片">
                    <div class="absolute inset-0 bg-black bg-opacity-50 rounded-xl flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                        <span class="text-white">点击更换图片</span>
                    </div>
                </div>
            `;
            
            callback(base64Data);
            
            document.getElementById('resultContainer').classList.add('hidden');
            
        } catch (error) {
            console.error('处理文件时出错:', error);
            alert('处理图片时出错，请重试');
        }
    };
    
    reader.onerror = () => {
        console.error('读取文件时出错');
        alert('读取图片时出错，请重试');
    };
    
    reader.readAsDataURL(file);
}

function updateProgress(progress) {
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    
    progressContainer.classList.remove('hidden');
    progressBar.style.width = `${progress}%`;
}

function showResult(imageUrl) {
    const resultContainer = document.getElementById('resultContainer');
    const resultImage = document.getElementById('resultImage');
    const downloadButton = document.getElementById('downloadButton');
    
    resultImage.src = imageUrl;
    downloadButton.href = imageUrl;
    resultContainer.classList.remove('hidden');
    
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload('uploadPic1', 'pic1Input', (data) => {
        pic1Data = data;
    });
    
    setupFileUpload('uploadPic2', 'pic2Input', (data) => {
        pic2Data = data;
    });
    
    const swapButton = document.getElementById('swapButton');
    swapButton.addEventListener('click', async () => {
        if (!pic1Data || !pic2Data) {
            alert('请先上传两张图片');
            return;
        }
        
        try {
            swapButton.disabled = true;
            swapButton.textContent = '处理中...';
            swapButton.classList.add('opacity-75');
            
            updateProgress(30);
            
            const response = await fetch('/api/swap-face', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    pic1: pic1Data,
                    pic2: pic2Data
                })
            });
            
            updateProgress(70);
            
            const result = await response.json();
            if (result.success) {
                updateProgress(100);
                showResult(result.result_url);
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            alert('处理失败：' + error.message);
        } finally {
            swapButton.disabled = false;
            swapButton.textContent = '开始替换';
            swapButton.classList.remove('opacity-75');
        }
    });
}); 