import StickyBox from 'react-sticky-box'
const React = require('react')
const $ = require('jquery')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')
let FilterNav = require('./FilterNav')
let ListMapSwitch = require('./MapListSwitch')

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      items: [],
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      showListMap: true,
      resizeMap: false,
      filterChanged: false,
      status: -1,
      participation: -1,
      district: props.selectedDistrict,
      topic: props.selectedTopic
    }
  }

  isInFilter (item) {
    return (this.state.topic === '-1' || this.state.topic === item.topic || this.state.topic.toLowerCase() === item.topic.toLowerCase()) &&
      (this.state.district === '-1' || this.state.district === item.district)
  }

  updateList () {
    let items = []
    this.props.initialitems.forEach((item, i) => {
      if (this.isInFilter(item)) {
        items.push(item)
      }
    })
    this.setState({
      items: items,
      filterChanged: false
    })
  }

  componentDidMount () {
    this.updateList()
  }

  componentDidUpdate () {
    if (this.state.filterChanged === true) {
      this.updateList()
    }
  }

  toggleSwitch () {
    let newValue = !this.state.showListMap
    this.setState({ showListMap: newValue })
  }

  hideMap (e) {
    e.preventDefault()
    $('#map').addClass('u-sm-down-display-none')
    $('#list').removeClass('u-sm-down-display-none')
  }

  selectDistrict (district) {
    var newDistrict = (district === '-1') ? '-1' : this.props.districtnames[district]
    this.setState({
      filterChanged: true,
      district: newDistrict
    })
  }

  selectTopic (topic) {
    this.setState({
      filterChanged: true,
      topic: topic
    })
  }

  hideList (e) {
    e.preventDefault()
    $('#list').addClass('u-sm-down-display-none')
    $('#map').removeClass('u-sm-down-display-none')
    $('#map').css('display', 'block')
    this.setState({ resizeMap: true })
  }

  render () {
    return (
      <div>
        <FilterNav
          selectDistrict={this.selectDistrict.bind(this)}
          selectTopic={this.selectTopic.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
        />
        <ListMapSwitch
          toggleSwitch={this.toggleSwitch.bind(this)}
          hideMap={this.hideMap.bind(this)}
          hideList={this.hideList.bind(this)}
        />
        { this.state.showListMap
          ? <div className="map-list-combined">
            <div id="list" className="list-container map-list-combined__list">
              <PlansList key="content" items={this.state.items} />
            </div>
            <div id="map" className="map-container map-list-combined__map u-sm-down-display-none">
              <StickyBox offsetTop={0} offsetBottom={0}>
                <PlansMap key="content"
                  resize={this.state.resizeMap}
                  items={this.state.items}
                  bounds={this.props.bounds}
                  districts={this.props.districts}
                  baseurl={this.props.baseurl}
                  districtnames={this.props.districtnames} />
              </StickyBox>
            </div>
          </div>
          : <div className="map-list-combined">
            <div className="list-container map-list-combined__list">
              <PlansList key="content" items={this.state.items} />
            </div>
          </div>
        }
      </div>
    )
  }
}

module.exports = ListMapBox
