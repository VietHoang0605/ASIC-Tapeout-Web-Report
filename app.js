// ==============================================================================
// LOGIC ĐIỀU KHIỂN BÁO CÁO KHÓA HỌC: ASIC SILICON TAPEOUT (SKYWATER 130NM)
// Quản lý Buổi 01..04+05, Sub-segments, Mục lục thông minh, Tìm kiếm & Lightbox
// ==============================================================================

const TapeoutApp = (function () {
  let activeSessionId = "buoi-04"; // Mặc định mở Buổi 4 & 5 (Lab 3) mới nhất
  let activeSubtab = "all"; // 'all', 'materials', 'lab_guide', 'student_report'
  let allTOCExpanded = false;

  // Trạng thái Lightbox tương tác
  let lightboxScale = 1.0;
  let isDragging = false;
  let startX = 0, startY = 0;
  let translateX = 0, translateY = 0;
  let mermaidRenderSeq = 0;

  function init() {
    const hash = window.location.hash.replace("#", "");
    if (hash.startsWith("buoi-04") || hash.startsWith("b4-")) {
      activeSessionId = "buoi-04";
    } else if (hash.startsWith("buoi-03") || hash.startsWith("b3-")) {
      activeSessionId = "buoi-03";
    } else if (hash.startsWith("buoi-02") || hash.startsWith("b2-")) {
      activeSessionId = "buoi-02";
    } else if (hash.startsWith("buoi-01") || hash.startsWith("b1-")) {
      activeSessionId = "buoi-01";
    } else {
      activeSessionId = "buoi-04";
    }

    renderKPIDeck();
    renderSessionTabs();
    renderCurrentSession();
    setupScrollProgress();
    setupKeyboardShortcuts();
    setupLightboxEvents();
  }

  function renderKPIDeck() {
    const container = document.getElementById("master-kpi-deck");
    if (!container || !COURSE_METADATA.kpis) return;

    let html = "";
    COURSE_METADATA.kpis.forEach((kpi) => {
      html += `
        <div class="kpi-card">
          <div class="kpi-num" style="color: ${kpi.color};">${kpi.value}</div>
          <div class="kpi-label">${kpi.label}</div>
          <div class="kpi-sub">${kpi.sub}</div>
        </div>
      `;
    });
    container.innerHTML = html;
  }

  function renderSessionTabs() {
    const container = document.getElementById("session-tabs-nav");
    if (!container) return;

    let html = "";
    SESSIONS_DATA.forEach((s) => {
      const isActive = s.id === activeSessionId ? "active" : "";
      html += `
        <button class="session-tab-btn ${isActive}" id="tab-btn-${s.id}" onclick="TapeoutApp.switchSession('${s.id}')">
          <span class="tab-badge">${s.badge}</span>
          <span class="tab-title">${s.shortTitle}</span>
        </button>
      `;
    });
    container.innerHTML = html;
  }

  function switchSession(sessionId) {
    if (activeSessionId === sessionId) return;
    activeSessionId = sessionId;
    activeSubtab = "all";

    document.querySelectorAll(".session-tab-btn").forEach((btn) => btn.classList.remove("active"));
    const activeBtn = document.getElementById(`tab-btn-${sessionId}`);
    if (activeBtn) activeBtn.classList.add("active");

    renderCurrentSession();
    scrollToAnchor("session-hero-container");
  }

  function postProcessStream(container) {
    if (!container) return;

    // 1. Convert <pre><code class="language-mermaid"> into <div class="mermaid"> cleanly
    const mermaidBlocks = container.querySelectorAll("pre code.language-mermaid, pre.mermaid");
    mermaidBlocks.forEach((codeEl) => {
      const preEl = codeEl.tagName === "PRE" ? codeEl : codeEl.parentElement;
      const mermaidDiv = document.createElement("div");
      mermaidDiv.className = "mermaid";
      mermaidDiv.textContent = codeEl.textContent.trim();
      mermaidDiv.title = "Nhấp để phóng to toàn màn hình";
      mermaidDiv.onclick = () => {
        const svg = mermaidDiv.querySelector("svg");
        if (svg) openSvgLightbox(svg);
      };
      preEl.replaceWith(mermaidDiv);
    });

    if (window.mermaid) {
      const nodes = Array.from(container.querySelectorAll(".mermaid"));
      if (nodes.length > 0) {
        Promise.all(
          nodes.map(async (node) => {
            const code = node.textContent.trim();
            if (!code) return;
            try {
              const id = `mermaid-svg-${++mermaidRenderSeq}`;
              const { svg, bindFunctions } = await mermaid.render(id, code);
              node.innerHTML = svg;
              if (typeof bindFunctions === "function") bindFunctions(node);
            } catch (err) {
              console.warn("Mermaid diagram warning:", err && err.str ? err.str : err);
            }
          })
        );
      }
    }

    // 2. Render MathJax
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([container]).catch((err) => {
        console.warn("MathJax typeset error:", err);
      });
    }
  }

  function renderCurrentSession() {
    const session = SESSIONS_DATA.find((s) => s.id === activeSessionId);
    if (!session) return;

    renderSessionHero(session);
    renderSubtabBar(session);
    renderMasterTOC(session);
    renderContentStream(session);
    renderQuickTOCDrawer(session);
  }

  function renderSessionHero(session) {
    const container = document.getElementById("session-hero-container");
    if (!container) return;

    let downloadsHtml = "";
    if (session.downloads && session.downloads.length > 0) {
      downloadsHtml = '<div class="asset-deck">';
      session.downloads.forEach((dl) => {
        downloadsHtml += `
          <div class="asset-card">
            <div class="asset-details">
              <div class="asset-title-row">
                <span class="asset-type-pill">${dl.type}</span>
                <span class="asset-name">${dl.name}</span>
                <span class="asset-size-pill">${dl.size}</span>
              </div>
              <p class="asset-desc">${dl.desc}</p>
            </div>
            <button class="btn-asset-download" onclick="TapeoutApp.alertDownload('${dl.name}')">
              Tải về
            </button>
          </div>
        `;
      });
      downloadsHtml += '</div>';
    }

    container.innerHTML = `
      <div class="week-hero-card">
        <div class="week-hero-header">
          <span class="week-badge-pill">${session.badge}</span>
          <span class="week-date-pill">Ngày học: ${session.date} · CTW SEMI</span>
        </div>
        <h2 class="week-hero-title">${session.tabTitle}</h2>
        <p class="week-hero-summary">${session.summary}</p>
        <div class="asset-section-wrap">
          <div class="asset-section-label">TÀI NGUYÊN ĐÍNH KÈM BUỔI HỌC</div>
          ${downloadsHtml}
        </div>
      </div>
    `;
  }

  function renderSubtabBar(session) {
    const container = document.getElementById("subtab-bar-nav");
    if (!container) return;

    const subtabs = [
      { id: "all", label: "Tất Cả Nội Dung", isHighlight: false },
      { id: "materials", label: "1. Tài Liệu & Giáo Trình", isHighlight: false },
      { id: "lab_guide", label: "2. Bài Hướng Dẫn Lab", isHighlight: false },
      { id: "student_report", label: "3. Báo Cáo Thực Chiến Học Viên", isHighlight: true }
    ];

    let html = "";
    subtabs.forEach((tab) => {
      const isActive = activeSubtab === tab.id ? "active" : "";
      const highlightClass = tab.isHighlight ? "highlight-report" : "";
      html += `
        <button class="subtab-pill ${isActive} ${highlightClass}" data-subtab="${tab.id}" onclick="TapeoutApp.filterSubtab('${tab.id}')">
          ${tab.label}
        </button>
      `;
    });

    container.innerHTML = html;
  }

  function filterSubtab(subtabId) {
    activeSubtab = subtabId;
    const session = SESSIONS_DATA.find((s) => s.id === activeSessionId);
    if (!session) return;

    document.querySelectorAll(".subtab-pill").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-subtab") === subtabId);
    });

    renderMasterTOC(session);
    renderContentStream(session);
  }

  function renderMasterTOC(session) {
    const container = document.getElementById("master-toc-list");
    if (!container) return;

    let filteredSections = session.subsections;
    if (activeSubtab !== "all") {
      const norm = activeSubtab.replace(/-/g, "_");
      filteredSections = session.subsections.filter((s) => s.id.replace(/-/g, "_").includes(norm));
    }

    let html = "";
    filteredSections.forEach((sec) => {
      let sublistHtml = "";
      if (sec.toc && sec.toc.length > 0) {
        sec.toc.forEach((item) => {
          const indentClass = item.level >= 3 ? "toc-level-3-link" : "";
          const bullet = item.level >= 3 ? "↳" : "•";
          sublistHtml += `
            <li>
              <a class="toc-sublink ${indentClass}" onclick="TapeoutApp.scrollToAnchor('${item.anchor}')">
                ${bullet} ${item.title}
              </a>
            </li>
          `;
        });
      }

      const subCount = sec.toc ? sec.toc.length : 0;
      html += `
        <div class="toc-chapter-item ${allTOCExpanded ? 'expanded' : ''}" id="toc-sec-item-${sec.id}">
          <div class="toc-chapter-header-btn" onclick="TapeoutApp.toggleTOCSection('${sec.id}')">
            <div class="toc-ch-title-wrap">
              <span class="toc-ch-title-text" onclick="event.stopPropagation(); TapeoutApp.scrollToAnchor('section-${sec.id}')">
                ${sec.title}
              </span>
            </div>
            <div class="toc-ch-right-controls">
              <span class="toc-ch-count-badge">${subCount}</span>
              <span class="toc-ch-toggle-arrow" id="toc-arrow-${sec.id}">▼</span>
            </div>
          </div>
          <ul class="toc-sublist" id="toc-sublist-${sec.id}" style="display: ${allTOCExpanded ? 'block' : 'none'};">
            ${sublistHtml}
          </ul>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  function toggleTOCSection(secId) {
    const item = document.getElementById(`toc-sec-item-${secId}`);
    const sublist = document.getElementById(`toc-sublist-${secId}`);
    if (!sublist) return;

    const isHidden = sublist.style.display === "none" || sublist.style.display === "";
    sublist.style.display = isHidden ? "block" : "none";
    if (item) item.classList.toggle("expanded", isHidden);
  }

  function toggleAllTOC() {
    allTOCExpanded = !allTOCExpanded;
    document.querySelectorAll(".toc-sublist").forEach((list) => {
      list.style.display = allTOCExpanded ? "block" : "none";
    });
    document.querySelectorAll(".toc-chapter-item").forEach((item) => {
      item.classList.toggle("expanded", allTOCExpanded);
    });

    const btn = document.getElementById("btn-toc-toggle-all");
    if (btn) {
      btn.innerHTML = allTOCExpanded
        ? '<span id="toc-toggle-icon">▲</span> Thu gọn tất cả đề mục'
        : '<span id="toc-toggle-icon">▼</span> Mở rộng tất cả đề mục';
    }
  }

  function renderContentStream(session) {
    const container = document.getElementById("session-content-stream");
    if (!container) return;

    let filteredSections = session.subsections;
    if (activeSubtab !== "all") {
      const norm = activeSubtab.replace(/-/g, "_");
      filteredSections = session.subsections.filter((s) => s.id.replace(/-/g, "_").includes(norm));
    }

    let html = "";
    filteredSections.forEach((sec) => {
      html += `
        <article class="chapter-stream-block" id="section-${sec.id}">
          <div class="topic-hero-card">
            <button class="btn-back-to-toc-inline" onclick="TapeoutApp.scrollToAnchor('master-toc-container')" title="Về bảng mục lục">
              ↑ Mục lục
            </button>
            <div class="topic-meta-row">
              <span class="topic-badge">${sec.category}</span>
              <span class="topic-category-tag">${sec.readTime} đọc</span>
            </div>
            <h2 class="topic-hero-title">${sec.title}</h2>
            <p class="topic-hero-summary">${sec.summary}</p>
          </div>

          <div class="chapter-body-content">
            ${sec.htmlContent}
          </div>
        </article>
      `;
    });

    container.innerHTML = html;
    postProcessStream(container);
  }

  function renderQuickTOCDrawer(session) {
    const container = document.getElementById("quick-toc-drawer-body");
    if (!container) return;

    let html = "";
    session.subsections.forEach((sec) => {
      html += `
        <div class="drawer-chapter-group">
          <div class="drawer-ch-title" onclick="TapeoutApp.closeQuickTOC(); TapeoutApp.scrollToAnchor('section-${sec.id}')">
            ${sec.title}
          </div>
          <ul class="drawer-sub-list">
      `;
      if (sec.toc && sec.toc.length > 0) {
        sec.toc.forEach((item) => {
          const cls = item.level >= 3 ? "drawer-sub-link drawer-sub-l3" : "drawer-sub-link";
          html += `
            <li>
              <a class="${cls}" href="#${item.anchor}" onclick="TapeoutApp.closeQuickTOC()">
                ${item.level >= 3 ? "↳" : "•"} ${item.title}
              </a>
            </li>
          `;
        });
      }
      html += `</ul></div>`;
    });

    container.innerHTML = html;
  }

  function scrollToAnchor(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openQuickTOC() {
    const modal = document.getElementById("quick-toc-modal");
    if (modal) modal.classList.add("active");
  }

  function closeQuickTOC() {
    const modal = document.getElementById("quick-toc-modal");
    if (modal) modal.classList.remove("active");
  }

  function setupScrollProgress() {
    window.addEventListener("scroll", () => {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      const bar = document.getElementById("read-progress-bar");
      if (bar) bar.style.width = scrolled + "%";
    });
  }

  function updateLightboxTransform() {
    const img = document.getElementById("lightbox-img-element");
    if (img) {
      img.style.transform = `translate(${translateX}px, ${translateY}px) scale(${lightboxScale})`;
    }
  }

  function resetLightbox() {
    lightboxScale = 1.0;
    translateX = 0;
    translateY = 0;
    updateLightboxTransform();
  }

  function openSvgLightbox(svgElement) {
    const lightbox = document.getElementById("img-lightbox");
    const lightboxImg = document.getElementById("lightbox-img-element");
    if (!lightbox || !lightboxImg) return;

    const clonedSvg = svgElement.cloneNode(true);
    if (!clonedSvg.getAttribute("xmlns")) {
      clonedSvg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    }
    clonedSvg.style.backgroundColor = "#ffffff";
    const svgData = new XMLSerializer().serializeToString(clonedSvg);
    const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
    const url = (window.URL || window.webkitURL || window).createObjectURL(svgBlob);

    lightboxImg.style.background = "#ffffff";
    const rect = svgElement.getBoundingClientRect();
    const isPortrait = rect.height > rect.width * 1.15;
    lightboxImg.style.width = isPortrait ? "auto" : "88vw";
    lightboxImg.style.height = isPortrait ? "82vh" : "auto";
    lightboxImg.src = url;
    resetLightbox();
    lightbox.classList.add("active");
  }

  function setupLightboxEvents() {
    const lightbox = document.getElementById("img-lightbox");
    const lightboxImg = document.getElementById("lightbox-img-element");
    const closeBtn = document.getElementById("lightbox-close");

    document.addEventListener("click", (e) => {
      const target = e.target;
      if (target.classList.contains("responsive-diagram-img") || target.closest(".interactive-diagram-card img")) {
        const img = target.tagName === "IMG" ? target : target.querySelector("img");
        if (img && lightbox && lightboxImg) {
          const srcLower = (img.getAttribute("src") || "").toLowerCase();
          const wrapBg = img.closest(".diagram-img-wrap")?.style.backgroundColor || "";
          const isDarkBg = wrapBg.includes("15, 23, 42") || srcLower.includes("counter_") || srcLower.includes("floorplan_") || srcLower.includes("yosys_") || srcLower.includes("liberty_") || srcLower.includes("rca_") || srcLower.includes("bon_nhom") || srcLower.includes("cau_truc") || srcLower.includes("cay_xung") || srcLower.includes("cts_can") || srcLower.includes("hien_tuong") || srcLower.includes("kien_truc") || srcLower.includes("mo_hinh") || srcLower.includes("phuong_phap") || srcLower.includes("so_do_thoi_gian");
          lightboxImg.style.background = isDarkBg ? "#0f172a" : "#ffffff";
          lightboxImg.style.width = srcLower.endsWith(".svg") ? "88vw" : "";
          lightboxImg.style.height = srcLower.endsWith(".svg") ? "auto" : "";
          lightboxImg.src = img.src;
          resetLightbox();
          lightbox.classList.add("active");
        }
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        lightbox.classList.remove("active");
        resetLightbox();
      });
    }

    if (lightbox) {
      lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) {
          lightbox.classList.remove("active");
          resetLightbox();
        }
      });

      lightbox.addEventListener("wheel", (e) => {
        e.preventDefault();
        const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
        lightboxScale = Math.min(Math.max(lightboxScale * zoomFactor, 0.4), 6.0);
        updateLightboxTransform();
      }, { passive: false });

      lightboxImg.addEventListener("mousedown", (e) => {
        if (e.button !== 0) return;
        isDragging = true;
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
        lightboxImg.style.cursor = "grabbing";
        e.preventDefault();
      });

      window.addEventListener("mousemove", (e) => {
        if (!isDragging) return;
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        updateLightboxTransform();
      });

      window.addEventListener("mouseup", () => {
        if (isDragging) {
          isDragging = false;
          if (lightboxImg) lightboxImg.style.cursor = "grab";
        }
      });
    }
  }

  function setupKeyboardShortcuts() {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        const lightbox = document.getElementById("img-lightbox");
        if (lightbox && lightbox.classList.contains("active")) {
          lightbox.classList.remove("active");
          resetLightbox();
        }
        closeQuickTOC();
      }
      if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
        e.preventDefault();
        const searchInput = document.getElementById("quick-search-input");
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
    });
  }

  function searchContent(query) {
    query = query.trim().toLowerCase();
    const clearBtn = document.getElementById("search-clear-btn");
    if (clearBtn) clearBtn.style.display = query ? "inline-block" : "none";

    if (!query) {
      renderCurrentSession();
      return;
    }

    document.querySelectorAll(".chapter-stream-block").forEach((block) => {
      const text = block.innerText.toLowerCase();
      block.style.display = text.includes(query) ? "block" : "none";
    });
  }

  function clearSearch() {
    const input = document.getElementById("quick-search-input");
    if (input) input.value = "";
    searchContent("");
  }

  function alertDownload(name) {
    alert(`File "${name}" đã sẵn sàng trong thư mục bài giảng gốc D:\\Tapeout_chip.`);
  }

  return {
    init,
    switchSession,
    filterSubtab,
    toggleTOCSection,
    toggleAllTOC,
    scrollToAnchor,
    scrollToTop,
    openQuickTOC,
    closeQuickTOC,
    searchContent,
    clearSearch,
    alertDownload
  };
})();

document.addEventListener("DOMContentLoaded", TapeoutApp.init);
