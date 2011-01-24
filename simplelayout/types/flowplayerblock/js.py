from collective.flowplayer.browser.view import JavaScript
import simplejson


class SlJavaScript(JavaScript): 
    """We use slightly diffrent JS implementation of collective.flowplayer
    """


    def __call__(self, request=None, response=None):
        """ Returns global configuration of the Flowplayer taken 
        from portal_properties
        """
        self.update()
        self.request.response.setHeader("Content-type", "text/javascript")

        return """(function($) {
        if (typeof(simplelayout) === 'undefined'){
            simplelayout = new Object;
        }
        simplelayout.loadFlowplayer = function($el){
            $('.autoFlowPlayer', $el).each(function() {
                var config = %(config)s;
                var $self = $(this);
                if ($self.is('.minimal')) { 
                    config.plugins.controls = null; 
                };
                var audio = $self.is('.audio');
                if (audio && !$self.is('.minimal')) {
                    if ($self.is('.image-left') || $self.is('.image-right'))
                        $self.width(230)
                    else
                        $self.width(500);
                    config.plugins.controls.all = false;
                    config.plugins.controls.play = true;
                    config.plugins.controls.scrubber = true;
                    config.plugins.controls.mute = true;
                    config.plugins.controls.volume = true;
                    config.plugins.controls.time = true;
                }
                if ($self.is('div')) {
                    // comming from Kupu, there are relative urls
                    config.clip.baseUrl = $('base').attr('href');
                    config.clip.url = $self.find('a').attr('href');
                    if (audio) {
                      // force .mp3 extension
                      config.clip.url = config.clip.url + '?e=.mp3';
                    };
                    // Ignore global autoplay settings
                    if ($self.find('img').length == 0) {
                        // no image. Don't autoplay, remove all elements inside the div to show player directly.
                        config.clip.autoPlay = false;
                        $self.empty();
                    } else {
                        // Clip is probably linked as image, so autoplay the clip after image is clicked
                        config.clip.autoPlay = true;
                    }
                }
                flowplayer(this, %(params)s, config)%(events)s;
                $('.flowPlayerMessage').remove();
            });
            $('.playListFlowPlayer', $el).each(function() {
                var config = %(config)s;
                var $self = $(this);
                var audio = $self.is('.audio');
                if (audio) { config.plugins.controls.fullscreen = false; }
                if ($self.is('.minimal')) { config.plugins.controls = null; }
                if ($self.find('img').length > 0) { 
                    // has splash
                    config.clip.autoPlay = true;
                }
                portlet_parents = $self.parents('.portlet');
                var playlist_selector = 'div#flowPlaylist';
                if (portlet_parents.length > 0) {
                    var portlet = true;
                    // playlist has to be bound to unique item
                    playlist_selector_id = portlet_parents.parent().attr('id')+'-playlist';
                    $self.parent().find('.flowPlaylist-portlet-marker').attr('id', playlist_selector_id);
                    playlist_selector = '#'+playlist_selector_id;
                    if (audio && !$self.is('.minimal')) {
                        config.plugins.controls.all = false;
                        config.plugins.controls.play = true;
                        config.plugins.controls.scrubber = true;
                        config.plugins.controls.mute = true;
                        config.plugins.controls.volume = false;
                    }
                } else {
                    var portlet = false;
                }
                if (!portlet) {
                    $("#pl").scrollable({items:playlist_selector, size:4, clickable:false});
                }
                // manual = playlist is setup using HTML tags, not using playlist array in config
                flowplayer(this, %(params)s, config).playlist(playlist_selector, {loop: true, manual: true})%(events)s;
                $self.show();
                $('.flowPlayerMessage').remove();

            });


        
        }
        
        $(function() { 
            simplelayout.loadFlowplayer(jq('body'));
            jq(".simplelayout-content:first").bind('refreshed',function(e, $el){
                simplelayout.loadFlowplayer($el);
            })
            
        });
})(jQuery);
""" % dict(params = simplejson.dumps(self.flash_properties_as_dict),
           config = simplejson.dumps(self.flowplayer_properties_as_dict, indent=4),
           events = self.events,
          )
