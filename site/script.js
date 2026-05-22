const nav = document.querySelector(".nav");
const menuButton = document.querySelector(".menu-button");
const languageMenus = document.querySelectorAll(".language-menu");

if (nav && menuButton) {
  menuButton.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });
}

languageMenus.forEach((menu) => {
  const toggle = menu.querySelector(".language-toggle");
  const options = menu.querySelectorAll("[data-language]");

  if (!toggle) {
    return;
  }

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  options.forEach((option) => {
    option.addEventListener("click", () => {
      const selectedLanguage = option.getAttribute("data-language");
      menu.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");

      if (selectedLanguage === "lt") {
        window.alert("Lithuanian version coming soon.");
      }
    });
  });
});

document.addEventListener("click", () => {
  languageMenus.forEach((menu) => {
    menu.classList.remove("open");
    const toggle = menu.querySelector(".language-toggle");
    if (toggle) {
      toggle.setAttribute("aria-expanded", "false");
    }
  });
});

function showFormMessage(form, message, isError = false) {
  const target = form.querySelector(".form-message");
  if (!target) return;
  target.textContent = message;
  target.classList.toggle("error", isError);
  target.classList.toggle("success", !isError);
}

function friendlyApiError(error) {
  const message = String(error && error.message ? error.message : error || "");

  if (message.includes("API_NOT_JSON") || message.includes("Unexpected token")) {
    return "FeeHunt could not reach the signup service right now. Your information was not lost. Please try again in a moment.";
  }

  if (message.includes("Failed to fetch") || message.includes("NetworkError") || message.includes("Load failed")) {
    return "FeeHunt could not connect to the signup service. Your information was not lost. Please check your connection and try again.";
  }

  if (message.includes("email_delivery_issue")) {
    return "FeeHunt created your trial, but could not send the license email right now. Please try Log in / Resend key in a moment.";
  }

  if (message.includes("license_creation_issue")) {
    return "FeeHunt could not create your license key right now. Your information was not lost. Please try again in a moment.";
  }

  if (message.includes("account_setup_issue")) {
    return "FeeHunt signup is not fully connected right now. Please try again in a moment.";
  }

  return message || "FeeHunt could not complete signup right now. Your information was not lost. Please try again in a moment.";
}

async function postJson(url, data, token = null) {
  const headers = { "content-type": "application/json" };
  if (token) headers.authorization = `Bearer ${token}`;
  const response = await fetch(url, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    const text = await response.text().catch(() => "");
    console.error("FeeHunt API returned a non-JSON response", {
      url,
      status: response.status,
      contentType,
      preview: text.slice(0, 160),
    });
    throw new Error("API_NOT_JSON");
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.ok === false) {
    const code = body.code ? `${body.code}: ` : "";
    throw new Error(code + (body.error || body.message || ""));
  }
  return body;
}

document.querySelectorAll("[data-api-form]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const type = form.getAttribute("data-api-form");
    const data = Object.fromEntries(new FormData(form).entries());
    const button = form.querySelector("button[type='submit']");
    if (button) button.disabled = true;

    try {
      if (type === "register") {
        const result = await postJson("/api/register-trial", data);
        showFormMessage(form, result.message || "Your trial has started. Please check your email for the license key.");
      }
      if (type === "login") {
        const result = await postJson("/api/login", data);
        showFormMessage(form, result.message || "Your FeeHunt license key was sent to your email.");
      }
    } catch (error) {
      console.error("FeeHunt signup flow failed", error);
      showFormMessage(form, friendlyApiError(error), true);
    } finally {
      if (button) button.disabled = false;
    }
  });
});
