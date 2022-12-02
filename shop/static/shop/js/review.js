class Review {
	constructor() {
		this.url = document.getElementById('review-js').getAttribute('review-url');
		this.nextURL = null;
		this.reviewBlock = document.getElementById('review-block');
		this.moreBtn = document.getElementById('review-more');
		this.config = {headers: {'Content-Type': 'multipart/form-data'}};

		axios.defaults.xsrfCookieName = 'csrftoken';
		axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	}

	showMoreBtn() {
		this.moreBtn.classList.remove('d-none');
	}
	
	hideMoreBtn() {
		this.moreBtn.classList.add('d-none');
	}
	
	checkMoreBtn() {
		return this.moreBtn.classList.contains('d-none');
	}

	getReveiwsEle() {
		return this.reviewBlock.querySelectorAll('.review');
	}

	makeImageEle(data) {
		let results = ``;

		if (data.length > 0) {
			data.forEach(e => {
				results += `<img src="${e.image}" style="width: 100px; height: 100px;">`;
			})
		}
		return results
	}

	makeDeleteBtnEle(data) {
		if (data.is_mine) {
			return `<a href="#"
				class="review-delete"
				data-review-id="${data.id}">
				삭제
			</a>`;
		} else {
			return '';
		}
	}

	makeReviewEle(data) {
		return `
			<div id="review-${data.id}" class="review">
				<p>${data.username}<small>${data.created_at}</small></p>
				<p>${this.makeDeleteBtnEle(data)}</p>
				<p>${data.rating}</p>
				<p>${data.review}</p>
				<p>${this.makeImageEle(data.images)}</p>
			</div>`; 
	}

	insertHTMLHandler(data, position) {
		if ( position == 'beforeend') {
			data.forEach(d => {
				this.reviewBlock.insertAdjacentHTML(
					position, this.makeReviewEle(d));
			});
		} else {
			this.reviewBlock.insertAdjacentHTML(
				position, this.makeReviewEle(data));
		}

		this.reviewBlock.querySelectorAll('.review-delete').forEach(ele => {
			ele.addEventListener('click', e => this.deleteReview(e, this))
		})
	}

	async getReviews() {
		const url = this.nextURL != null ? this.nextURL : this.url;

		try {
			const response = await axios.get(url);
	
			if (response.data.results.length > 0) {
				this.nextURL = response.data.next;

				this.insertHTMLHandler(response.data.results, 'beforeend');

				this.showMoreBtn();

				if (this.nextURL == null) { this.moreBtn.disabled = true; }

			} else {
				this.reviewBlock.innerHTML = '<p>no reviews</p>';
			}
		} catch(err) {
			console.error(err);
		}
	}

	addReview(e, self) {
		e.preventDefault();

		const data = new FormData(e.target);

		axios.post(self.url, data, self.config)
			.then(function (response) {
				if ( self.getReveiwsEle().length == 0 ) {
					self.reviewBlock.querySelector('p').remove();
				}

				self.insertHTMLHandler(response.data, 'afterbegin');
				e.target.reset();
			})
			.catch(function (err) {
				console.error(err);
			})
	}

	deleteReview(e, self) {
		e.preventDefault();

		const reviewId = e.currentTarget.getAttribute('data-review-id');
		
		if (confirm("정말 삭제하시겠습니다?")) {
			axios.delete(self.url, {data: {'review_id': reviewId,}})
				.then(function (response) {
					document.getElementById(`review-${reviewId}`).remove();

					if ( self.getReveiwsEle().length == 0 ) {
						self.reviewBlock.innerHTML = '<p>no reviews</p>';
						if (!self.checkMoreBtn()) { self.hideMoreBtn(); }
					}
				}).catch(function (err) {
					console.error(err);
				})
		}
	}
}

const reviewForm = document.getElementById('review-form');
const reviewMore = document.getElementById('review-more');

const review = new Review();
review.getReviews();

if (reviewForm) {
	reviewForm.addEventListener('submit', e => review.addReview(e, review));
}

reviewMore.addEventListener('click', () => review.getReviews());