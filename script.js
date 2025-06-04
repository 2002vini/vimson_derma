const jobs = [
    {
      title: "Frontend Developer",
      experience: "1-3 Years",
      openings: 2
    },
    {
      title: "Backend Developer",
      experience: "2-4 Years",
      openings: 1
    },
    {
      title: "UI/UX Designer",
      experience: "1-2 Years",
      openings: 1
    },
    {
      title: "Project Manager",
      experience: "3-5 Years",
      openings: 1
    },
    {
      title: "QA Engineer",
      experience: "1-2 Years",
      openings: 2
    },
    {
      title: "DevOps Engineer",
      experience: "2-5 Years",
      openings: 1
    },
    {
      title: "Product Owner",
      experience: "4-6 Years",
      openings: 1
    },
    {
      title: "Data Scientist",
      experience: "2-4 Years",
      openings: 2
    }
  ];
  
  const carouselInner = document.getElementById('carouselInner');
  const carouselIndicators = document.getElementById('carouselIndicators');
  
  // Clear existing content (in case of resize handling in future)
  carouselInner.innerHTML = '';
  carouselIndicators.innerHTML = '';
  
  const isMobile = window.innerWidth < 768;
  
  let slideCount = 0;
  
  if (isMobile) {
    // 1 card per slide on mobile
    jobs.forEach((job, i) => {
      const carouselItem = document.createElement('div');
      carouselItem.className = 'carousel-item';
      if (i === 0) carouselItem.classList.add('active');
  
      const row = document.createElement('div');
      row.className = 'row justify-content-center';
  
      const col = document.createElement('div');
      col.className = 'col-10 mb-3';
  
      col.innerHTML = `
        <div class="card job-card text-center h-100">
          <div class="icon-box mx-auto">
            <i class="bi bi-person"></i>
          </div>
          <div class="job-description">
          <h5 class="mt-2">${job.title}</h5>
          <p class="small text-muted">Experience: ${job.experience} | No. of Openings: ${job.openings}</p>
          </div>
          <button class="btn btn-primary apply-btn mt-2">Apply</button>
        </div>
      `;
      row.appendChild(col);
      carouselItem.appendChild(row);
      carouselInner.appendChild(carouselItem);
  
      // Pagination dot
      const indicator = document.createElement('button');
      indicator.setAttribute('type', 'button');
      indicator.setAttribute('data-bs-target', '#jobCarousel');
      indicator.setAttribute('data-bs-slide-to', slideCount);
      if (slideCount === 0) indicator.classList.add('active');
      carouselIndicators.appendChild(indicator);
  
      slideCount++;
    });
  } else {
    // Desktop: 4 cards per slide (2 rows × 2 cols)
    for (let i = 0; i < jobs.length; i += 4) {
      const carouselItem = document.createElement('div');
      carouselItem.className = 'carousel-item';
      if (i === 0) carouselItem.classList.add('active');
  
      for (let rowIndex = 0; rowIndex < 2; rowIndex++) {
        const row = document.createElement('div');
        row.className = 'row justify-content-center';
  
        for (let colIndex = 0; colIndex < 2; colIndex++) {
          const jobIndex = i + (rowIndex * 2) + colIndex;
          if (jobs[jobIndex]) {
            const col = document.createElement('div');
            col.className = 'col-md-6 card-col mb-3';
  
            col.innerHTML = `
              <div class="card job-card text-center h-100">
                <div class="icon-box mx-auto">
                  <i class="bi bi-person"></i>
                </div>
                <h5 class="mt-2">${jobs[jobIndex].title}</h5>
                <p class="small text-muted">Experience: ${jobs[jobIndex].experience} | No. of Openings: ${jobs[jobIndex].openings}</p>
                <button class="btn btn-primary apply-btn mt-2">Apply</button>
              </div>
            `;
            row.appendChild(col);
          }
        }
        carouselItem.appendChild(row);
      }
  
      carouselInner.appendChild(carouselItem);
  
      const indicator = document.createElement('button');
      indicator.setAttribute('type', 'button');
      indicator.setAttribute('data-bs-target', '#jobCarousel');
      indicator.setAttribute('data-bs-slide-to', slideCount);
      if (slideCount === 0) indicator.classList.add('active');
      carouselIndicators.appendChild(indicator);
  
      slideCount++;
    }
  }
  