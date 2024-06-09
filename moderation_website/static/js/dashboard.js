function toggle() {
    const servers = document.querySelector(".servers");
    const leftContent = document.querySelector(".left-content");
    const rightContent = document.querySelector(".right-content");
  
    servers.dataset.toggle = servers.dataset.toggle === "true" ? "false" : "true";
    leftContent.dataset.toggle =
      leftContent.dataset.toggle === "true" ? "false" : "true";
    rightContent.dataset.toggle =
      rightContent.dataset.toggle === "true" ? "false" : "true";
  }