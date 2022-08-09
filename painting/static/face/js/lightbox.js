var painting = {
    init: function () {
        this._initPopup();
        this._initControls();
    },

    _popup: null,
    _sound: null,

    _initPopup: function () {
        this._popup = $('.popup-gallery').magnificPopup({
            delegate: '.mfp-image',
            type: 'image',

            tLoading: 'Loading image #%curr%...',
            mainClass: 'mfp-album-popup',

            gallery: {
                arrowMarkup: '<span title="%title%" class="mfp-arrow mfp-arrow-%dir%"><i class="fa fa-chevron-%dir% mfp-prevent-close slide-arrow"></i></span>',
                enabled: true,
                navigateByImgClick: true,
                preload: [0, 2],
            },

            image: {
                cursor: null,
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',

                titleSrc: $.proxy(function (item) {
                    var slideshow = this._popup.data('slideshow');
                    var icon = slideshow ? "pause" : "play";
                    var el = item.data.el;
                    return '<div>' +
                        el.attr('data-painting-details') +
                        '</div>'
                }, this),

                markup: '<div class="mfp-figure">' +
                '<div class="mfp-close"></div>' +
                '<div class="mfp-img-holder">' +
                '<div class="mfp-img"></div>' +
                '</div>' +
                '<div class="mfp-bottom-bar">' +
                '<div class="mfp-title"></div>' +
                '<div class="mfp-counter"></div>' +
                '</div>' +
                '</div>' +
                '<button class="btn btn-default mfp-show-original"><i class="fas fa-camera"></i> <span class="text">Show Original</span></button>' +
                '<div class="origin-image">' +
                '<div class="origin-image-container">' + 
                '<div class="btn btn-default mfp-close-original"><i class="fas fa-times-circle"></i> Close</div>' +
                '<img src="" class="mfp-original"></img>' +
                '</div>' +
                '</div>'
            },

            closeBtnInside: true,

            callbacks: {

                updateStatus: $.proxy(function () {
                    this._initImage();
                    this._initShowOriginal();   
                }, this),

                close: $.proxy(function () {
                    this._popup.removeData('slideshow');
                    history.pushState(null, null, $(".popup-gallery").data("url"));
                    console.log("closed");
                    $(document).attr("overflow", "auto");
                }, this),

                open: function () {
                    var mfp = $.magnificPopup.instance;
                    var proto = $.magnificPopup.proto;

                    // extend function that moves to next item
                    mfp.next = function () {

                        // if index is not last, call parent method
                        if (mfp.index < mfp.items.length - 1) {
                            proto.next.call(mfp);
                            history.pushState(null, null, $($(".mfp-image")[mfp.index]).data("url"));
                        } else {
                            // otherwise do whatever you want, e.g. hide "next" arrow
                            proto.close();
                        }
                    };

                    // same with prev method
                    mfp.prev = function () {
                        if (mfp.index > 0) {
                            proto.prev.call(mfp);
                            history.pushState(null, null, $($(".mfp-image")[mfp.index]).data("url"));
                        }
                    };
                    $(document).attr("overflow", "hidden");
                }
            }
        });

        $.magnificPopup.instance.updateItemHTML = function () {
            var $this = this;
            var items = [];
            $.each($this.items, function (ii, item) {
                items.push({
                    src: $($("a.mfp-image")[ii]).attr("data-original-image-src"),
                    el: $($(".mfp-image")[ii])
                });
            });
            $this.items = items;
            $.magnificPopup.proto.updateItemHTML.call($this);
        }
    },


    _updateSlideshowButtonIcon: function () {
        var slideshow = this._popup.data('slideshow');
        var slideshowButton = $('.btn-slideshow i');
        if (slideshow) {
            slideshowButton.addClass('fa fa-pause');
            slideshowButton.removeClass('fa fa-play');
        } else {
            slideshowButton.addClass('fa fa-play');
            slideshowButton.removeClass('fa fa-pause');

        }

    },

    _initControls: function () {

        $('.album-controls').click($.proxy(function () {
            this._popup.data('slideshow', 'true');
            this._popup.magnificPopup('open');
        }, this));
    },

    _initImage: function () {
 
        $('.btn-fullscreen').on('click', function () {
            $('.mfp-container').addClass('mfp-container-fullscreen');
            return false;
        });

        $('.mfp-close-original').on('click', function (event) {
            event.stopPropagation();
            
            $('.origin-image').removeClass('active');
            $('.mfp-arrow').removeClass('hide');
        });

        $('.btn-slideshow').on('click', $.proxy(function () {
            var slideshow = this._popup.data("slideshow");
            if (slideshow) {
                this._popup.removeData('slideshow');
            } else {
                this._popup.data('slideshow', 'true');
            }

            this._updateSlideshowButtonIcon();

            return false;
        }, this));

        $('.mfp-figure').on('click', function () {
            $('.mfp-container').removeClass('mfp-container-fullscreen');
        });

        var mfp = $.magnificPopup.instance;
        history.pushState(null, null, $($(".mfp-image")[mfp.index]).data("url"));
    },

    _initShowOriginal: function () {
        var mfp = $.magnificPopup.instance;
        var originImage = $($("a.mfp-image")[mfp.index]).attr("data-origin-image-src");
        if(originImage.trim() === '') {
            $('.mfp-show-original').hide();
        } else {
            $('.mfp-show-original').show();

            $('.mfp-show-original').on('click', function (event) {
                event.stopPropagation();
    
                var mfp = $.magnificPopup.instance;
                var originImage = $($("a.mfp-image")[mfp.index]).attr("data-origin-image-src");
    
                $('.mfp-original').attr('src', originImage);
                $('.origin-image').addClass('active');
                $('.mfp-arrow').addClass('hide');
            });
        }
    }
}

$(function () {
    painting.init();

    $(window).on("popstate", function () {
        window.history.back();
    });
});
