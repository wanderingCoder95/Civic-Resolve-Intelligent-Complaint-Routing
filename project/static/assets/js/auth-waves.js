(function () {
    const canvas = document.getElementById("bg-canvas");
    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
        return;
    }

    const bodyStyles = getComputedStyle(document.body);
    const waveColor = (bodyStyles.getPropertyValue("--wave-color") || "79, 123, 255").trim();
    const waveHeightOffset = Number.parseFloat(bodyStyles.getPropertyValue("--wave-height-offset")) || 0.8;

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    let waveAmplitude = height * 0.09;

    const waveFrequency = 0.005;
    const waveSpeed = 0.015;
    let step = 0;

    function resizeCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        waveAmplitude = height * 0.09;
    }

    function drawWave(phase, alpha, offsetShift) {
        ctx.beginPath();
        ctx.moveTo(0, height);

        for (let x = 0; x < width; x += 1) {
            const y = Math.sin(x * waveFrequency + phase) * waveAmplitude + (height * (waveHeightOffset + offsetShift));
            ctx.lineTo(x, y);
        }

        ctx.lineTo(width, height);
        ctx.closePath();
        ctx.fillStyle = `rgba(${waveColor}, ${alpha})`;
        ctx.fill();
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        step += waveSpeed;

        drawWave(step, 0.12, 0);
        drawWave(step + 1.4, 0.17, 0.03);
        drawWave(step + 2.8, 0.24, 0.06);

        requestAnimationFrame(animate);
    }

    window.addEventListener("resize", resizeCanvas);
    animate();
})();
