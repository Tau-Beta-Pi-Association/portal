function jsRecaptchaRefresh() {
    console.log('click');
    const captchas = document.querySelectorAll('img.captcha')

    function headers(options) {
        options = options || {}
        options.headers = options.headers || {}
        options.headers['X-Requested-With'] = 'XMLHttpRequest'
        return options
    }

    for (const captcha of captchas) {
        const anchor = document.createElement('a')
        anchor.href = '#void'
        anchor.classList.add('captcha-refresh')
        anchor.textContent = 'Refresh'
        anchor.addEventListener('click', ({ target }) => {
          const url = `${window.location.origin}/captcha/refresh/`
          let formEl = target.parentElement
      
          while (formEl && formEl.tagName.toLowerCase() !== 'form') {
            formEl = formEl.parentElement
          }
      
          fetch(url, headers())
            .then(res => res.json())
            .then(json => {
              formEl.querySelector('input[name="captcha_0"]').value = json.key
              captcha.setAttribute('src', json.image_url)
              document.getElementById('audioSource').setAttribute('src', json.audio_url)
              document.getElementById('audio').load()
            })
            .catch(console.error)
      
          return false
        })
      
        captcha.after(anchor)
      }
    }