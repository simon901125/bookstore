(function () {
  const CURRENT_MEMBER_KEY = "froggyCurrentMember";
  const MEMBER_JSON_URL = "/python/member.json";

  function getCurrentMember() {
    try {
      const member = JSON.parse(localStorage.getItem(CURRENT_MEMBER_KEY) || "null");
      return member && member.email ? member : null;
    } catch (error) {
      return null;
    }
  }

  async function fetchMembers() {
    try {
      const response = await fetch(MEMBER_JSON_URL, { cache: "no-store" });
      if (!response.ok) return [];
      const members = await response.json();
      return Array.isArray(members) ? members : [];
    } catch (error) {
      return [];
    }
  }

  async function hydrateCurrentMember() {
    const currentMember = getCurrentMember();
    if (!currentMember?.email) return null;

    const members = await fetchMembers();
    const matchedMember = members.find(
      (member) =>
        String(member.email || "").toLowerCase() === currentMember.email.toLowerCase()
    );

    if (!matchedMember) return currentMember;

    const nextMember = {
      email: matchedMember.email,
      nickname: matchedMember.nickname,
    };
    localStorage.setItem(CURRENT_MEMBER_KEY, JSON.stringify(nextMember));
    return nextMember;
  }

  function getPathFor(pageName) {
    const path = window.location.pathname.replace(/\\/g, "/");
    const fromWindowJp = path.includes("/window_jp/");

    const paths = fromWindowJp
      ? {
          login: "../froggy_login/login.html",
          homeLogin: "../../window/froggy_main/mainscreen.html?login=1",
          userAll: "../../window/froggy_user_all/user_all.html",
          order: "../../window/froggy_order/order.html",
          saving: "../../window/froggy_booksaving/booksaving.html",
          userInfo: "../../window/froggy_user_info/user_info.html",
          search: "../../window/froggy_searchingPage/searchingPage.html",
        }
      : {
          login: "../../window_jp/froggy_login/login.html",
          homeLogin: "../froggy_main/mainscreen.html?login=1",
          userAll: "../froggy_user_all/user_all.html",
          order: "../froggy_order/order.html",
          saving: "../froggy_booksaving/booksaving.html",
          userInfo: "../froggy_user_info/user_info.html",
          search: "../froggy_searchingPage/searchingPage.html",
        };

    return paths[pageName] || paths.userAll;
  }

  function injectAuthStyles() {
    if (document.getElementById("froggyAuthStyles")) return;

    const style = document.createElement("style");
    style.id = "froggyAuthStyles";
    style.textContent = `
      .froggy-auth-menu { position: relative; display: flex; align-items: center; }
      .froggy-auth-menu .froggy-auth-dropdown {
        display: none;
        position: absolute;
        top: 100%;
        right: 0;
        z-index: 120;
        width: 14rem;
        overflow: hidden;
        border: 1px solid rgba(196, 198, 207, 0.9);
        border-radius: 0.75rem;
        background: #ffffff;
        box-shadow: 0 20px 45px rgba(0, 32, 70, 0.16);
      }
      .froggy-auth-menu:hover .froggy-auth-dropdown { display: block; }
      .froggy-auth-dropdown a {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        color: #1b1c1a;
        font-size: 0.875rem;
        text-decoration: none;
        transition: background-color 0.2s ease;
      }
      .froggy-auth-dropdown a:hover { background: #f5f3ef; }
      .froggy-auth-dropdown .froggy-auth-logout { color: #ba1a1a; border-top: 1px solid #e4e2de; }
      .froggy-auth-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        max-width: 8rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    `;
    document.head.appendChild(style);
  }

  function ensureAuthWrapper(link) {
    if (link.closest(".froggy-auth-menu")) {
      const existingWrapper = link.closest(".froggy-auth-menu");
      removeLegacyDropdown(existingWrapper);
      return existingWrapper;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "froggy-auth-menu";
    link.parentNode.insertBefore(wrapper, link);
    wrapper.appendChild(link);
    removeLegacyDropdown(wrapper);
    return wrapper;
  }

  function removeLegacyDropdown(wrapper) {
    const legacyDropdown = wrapper.nextElementSibling;
    if (legacyDropdown?.classList.contains("user-menu-dropdown")) {
      legacyDropdown.remove();
    }
  }

  function ensureNicknameLabel(link, member) {
    const labelText = member?.nickname || member?.email || "會員登入";
    let textLabel = link.querySelector("[data-auth-nickname]");

    if (!textLabel) {
      textLabel = link.querySelector("span:not(.material-symbols-outlined)");
    }

    if (!textLabel) {
      textLabel = document.createElement("span");
      textLabel.dataset.authNickname = "true";
      textLabel.className = "froggy-auth-label";
      link.appendChild(textLabel);
    }

    textLabel.textContent = labelText;
  }

  function renderMemberDropdown(wrapper) {
    let dropdown = wrapper.querySelector(".froggy-auth-dropdown");
    if (!dropdown) {
      dropdown = document.createElement("div");
      dropdown.className = "froggy-auth-dropdown";
      wrapper.appendChild(dropdown);
    }

    dropdown.innerHTML = `
      <a href="${getPathFor("userAll")}">
        <span class="material-symbols-outlined text-lg">space_dashboard</span>
        <span>總覽</span>
      </a>
      <a href="${getPathFor("order")}">
        <span class="material-symbols-outlined text-lg">receipt_long</span>
        <span>訂單詳情</span>
      </a>
      <a href="${getPathFor("saving")}">
        <span class="material-symbols-outlined text-lg">favorite</span>
        <span>收藏書</span>
      </a>
      <a href="${getPathFor("userInfo")}">
        <span class="material-symbols-outlined text-lg">edit_note</span>
        <span>會員資料修改</span>
      </a>
      <a href="#" class="froggy-auth-logout" data-auth-logout>
        <span class="material-symbols-outlined text-lg">logout</span>
        <span>登出</span>
      </a>
    `;
  }

  function removeMemberDropdown(link) {
    link.closest(".froggy-auth-menu")?.querySelector(".froggy-auth-dropdown")?.remove();
  }

  function showModalLoginMessage(form, message, type = "error") {
    let box = form.querySelector("[data-login-message]");
    if (!box) {
      box = document.createElement("p");
      box.dataset.loginMessage = "true";
      form.prepend(box);
    }

    box.textContent = message;
    box.className =
      "rounded-lg border px-4 py-3 text-sm font-body " +
      (type === "success"
        ? "border-green-200 bg-green-50 text-green-700"
        : "border-red-200 bg-red-50 text-red-700");
  }

  function getLoginFormFields(form) {
    const emailInput =
      form.querySelector("#loginEmail") ||
      form.querySelector("input[type='email']") ||
      form.querySelector("input[type='text']");
    const passwordInput =
      form.querySelector("#loginPassword") || form.querySelector("input[type='password']");
    return { emailInput, passwordInput };
  }

  function closeLoginModal(form) {
    const modal = form.closest("#loginModal");
    if (modal) {
      modal.style.display = "none";
    }
  }

  function bindLoginModalForms() {
    document.querySelectorAll("#loginModal form").forEach((form) => {
      if (form.dataset.authLoginBound) return;
      form.dataset.authLoginBound = "true";

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const { emailInput, passwordInput } = getLoginFormFields(form);
        const email = emailInput?.value.trim().toLowerCase() || "";
        const password = passwordInput?.value || "";

        if (!email || !password) {
          showModalLoginMessage(form, "請輸入電子郵件與密碼。");
          return;
        }

        const members = await fetchMembers();
        const matchedMember = members.find(
          (member) =>
            String(member.email || "").toLowerCase() === email &&
            String(member.password || "") === password
        );

        if (!matchedMember) {
          showModalLoginMessage(form, "帳號或密碼錯誤。");
          return;
        }

        localStorage.setItem(
          CURRENT_MEMBER_KEY,
          JSON.stringify({
            email: matchedMember.email,
            nickname: matchedMember.nickname,
          })
        );
        showModalLoginMessage(form, "登入成功。", "success");
        window.alert("登入成功，歡迎回來！");
        closeLoginModal(form);
        updateMemberLinks();
      });
    });
  }

  function updateMemberLinks() {
    injectAuthStyles();
    const member = getCurrentMember();
    const loginModal = document.getElementById("loginModal");

    document.querySelectorAll("a").forEach((link) => {
      const hasPersonIcon = [...link.querySelectorAll(".material-symbols-outlined")].some(
        (icon) => icon.textContent.trim() === "person"
      );
      const isLoginLink = link.href.includes("froggy_login/login.html");
      const isUserAllLink = link.href.includes("froggy_user_all/user_all.html");
      const isKnownAuthLink = Boolean(link.dataset.authState);
      if (!hasPersonIcon || (!isLoginLink && !isUserAllLink && !isKnownAuthLink)) return;

      const wrapper = ensureAuthWrapper(link);
      link.href = member ? getPathFor("userAll") : loginModal ? "#" : getPathFor("login");
      link.title = member ? "會員中心" : "會員登入";
      link.dataset.authState = member ? "logged-in" : "guest";
      ensureNicknameLabel(link, member);

      if (member) {
        renderMemberDropdown(wrapper);
      } else {
        removeMemberDropdown(link);
      }

      if (!link.dataset.authClickBound) {
        link.dataset.authClickBound = "true";
        link.addEventListener(
          "click",
          (event) => {
            const currentMember = getCurrentMember();
            if (currentMember) {
              event.preventDefault();
              window.location.href = getPathFor("userAll");
              return;
            }

            if (loginModal) {
              event.preventDefault();
              loginModal.style.display = "flex";
            }
          },
          true
        );
      }
    });

    bindLogoutLinks();
  }

  function guardMemberPages() {
    const path = window.location.pathname.replace(/\\/g, "/");
    const isMemberPage =
      path.includes("/froggy_user_all/") ||
      path.includes("/froggy_user_info/") ||
      path.includes("/froggy_order/") ||
      path.includes("/froggy_booksaving/");
    if (!isMemberPage || getCurrentMember()) return;

    window.location.replace(getPathFor("homeLogin"));
  }

  function bindLogoutLinks() {
    document.querySelectorAll("[data-auth-logout]").forEach((link) => {
      if (link.dataset.logoutBound) return;
      link.dataset.logoutBound = "true";
      link.addEventListener("click", (event) => {
        event.preventDefault();
        localStorage.removeItem(CURRENT_MEMBER_KEY);
        window.location.replace(getPathFor("homeLogin"));
      });
    });
  }

  function bindTopSearch() {
    document.querySelectorAll("nav input[placeholder*='搜尋']").forEach((input) => {
      if (input.dataset.authSearchBound) return;
      input.dataset.authSearchBound = "true";

      const container = input.closest("div");
      const button = container?.querySelector("button");
      const submitSearch = () => {
        const query = input.value.trim();
        if (!query) return;
        window.location.href = `${getPathFor("search")}?q=${encodeURIComponent(query)}`;
      };

      button?.addEventListener("click", submitSearch);
      input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          submitSearch();
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    bindLoginModalForms();
    bindTopSearch();
    hydrateCurrentMember().finally(updateMemberLinks);
    guardMemberPages();
  });

  window.FroggyAuth = {
    getCurrentMember,
    updateMemberLinks,
  };
})();
