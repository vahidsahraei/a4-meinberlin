/* global django */
const React = require('react')
const $ = require('jquery')

class PopUp extends React.Component {
  escapeHtml (unsafe) {
    return $('<div>').text(unsafe).html()
  }

  render () {
    let statusClass = (this.props.item.participation_active === true) ? 'maplist-item__status-active' : 'maplist-item__status-inactive'
    if (this.props.item.type === 'project') {
      return (
        <div className="maps-popups-popup-text-content">
          <span className="label label--secondary maplist-item__label u-spacer-bottom-half">{this.props.itemTopic}</span>
          <span className="maplist-popup-item__roofline">{this.props.item.district}</span>
          <div className="maps-popups-popup-name u-spacer-bottom-half">
            <a href={this.props.item.url}>{this.props.item.title}</a>
          </div>
          {this.props.item.future_phase &&
          <div className="status-item-popup status__future">
            <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('Participation: from ') + this.props.item.future_phase + django.gettext(' possible')}</span>
          </div>
          }
          {this.props.item.active_phase &&
          <div className="status-item-popup status__active">
            <div className="status-bar__active"><span className="status-bar__active-fill" /></div>
            <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('remaining')} {this.props.item.active_phase[1]}</span>
          </div>
          }
          {this.props.item.past_phase &&
            <div className="status-item-popup status-bar__past">
              {django.gettext('Participation ended. Read result.')}
            </div>
          }
          {this.props.item.plan_url &&
            <a href={this.props.item.plan_url}>{this.props.item.plan_title}</a>
          }
        </div>
      )
    } else {
      return (
        <div className="maps-popups-popup-text-content">
          {this.props.item.topic &&
          <div className="maplist-item__labels u-spacer-bottom-half">
            <span className="label label--secondary">{this.props.itemTopic}</span>
          </div>
          }
          <span className="maplist-item__roofline">{this.props.item.district}</span>
          <div className="maps-popups-popup-name u-spacer-bottom-half">
            <a href={this.props.item.url}>{this.props.item.title}</a>
          </div>
          <div className="maplist-popup-item__stats">
            <span className="maplist-item__proj-count">
              <i className="fas fa-th" />{django.gettext('Participation projects: ') }</span>
            <span>{this.props.item.published_projects_count}</span>
            <span className="maplist-item__status"><i className="fas fa-clock" />{django.gettext('Participation: ')}</span>
            <span className={statusClass}>{this.props.item.participation_string}</span>
          </div>
        </div>
      )
    }
  }
}

module.exports = PopUp
